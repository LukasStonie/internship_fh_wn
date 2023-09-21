import base64
import io

import numpy as np
import sqlalchemy.exc
from flask import render_template, request, url_for, flash, redirect
from flask_login import login_required
from matplotlib import pyplot as plt
from scipy.signal import find_peaks
import pandas as pd
from wtforms import FormField, FieldList, IntegerField, SelectField
from wtforms.validators import InputRequired

from app.forms.forms import PeakForm
from app.routes.peaks import bp

from app.models.model import Peak, Spectrum, Intensity

from app.extensions import db


def peak_exists(compound_id):
    """
        Checks if a peak spectrum already exists for a given compound

    Args:
        compound_id (int): id of the compound to check for

    Returns:
        True if a peak spectrum already exists, False otherwise
    """
    spectrum_type_peak = 3
    # check if peak spectrum already exists
    peak_spectrum = db.session.query(Spectrum).filter(Spectrum.compound_id == compound_id).filter(
        Spectrum.spectrum_type_id == spectrum_type_peak).first()
    if peak_spectrum is not None:
        flash('Es existiert bereits ein Peak-Spektrum für diese Substanz', 'danger')
        return True
    return False


def create_plot(peaks):
    """
        Creates a plot of the peaks with wavenumber on the x-axis and intensity on the y-axis, plot is stored in the plt object

    Args:
        peaks (np.array): two-dimensional numpy array with wavenumber and intensity

    Returns:
        None, plot is stored in the plt object
    """
    # plot peaks_array
    plt.plot(peaks[:, 0], peaks[:, 1])
    # describe axis
    plt.xlabel('Wavenumber ($\mathregular{cm^{-1}}$)')
    plt.ylabel('Intensity (-)')


def get_wavenumbers_and_img(compound_id):
    """
        Gets the wavenumbers of the peaks and the plot of the peak spectrum with the highest id for a given compound (latest added peak spectrum)

    Args:
        compound_id (int): id of the compound to get the peak spectrum for

    Returns:
        wavenumbers (np.array): one-dimensional numpy array with the wavenumbers of the peaks
        img (base64): base64 encoded image of the plot
    """
    # get the spectrum with the highest id
    spectrum = db.session.query(Spectrum).filter(Spectrum.compound_id == compound_id).order_by(
        Spectrum.id.desc()).first()

    # read the spectrum and transpose it -> needed for find_peaks
    data = pd.read_csv(spectrum.file_path, index_col=None).transpose()
    # find the peaks
    peaks = find_peaks(data.iloc[1, :])
    # get the wavenumbers of the peaks
    wavenumbers = data.iloc[0, peaks[0]]

    # create empty peaks_array
    peaks_array = np.zeros(data.shape[1])

    # iterate peaks
    for peak in peaks[0]:
        # peak is index in data
        # lookup peak height in data and store in peaks_array
        peaks_array[peak] = data.iloc[1, :][peak]

    combined = np.column_stack((data.iloc[0, :], peaks_array))
    # create plot
    create_plot(combined)

    img = io.BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)

    return wavenumbers, base64.b64encode(img.getvalue()).decode('utf8'), spectrum.file_path


@bp.route('/new/<compound_id>', methods=['GET'])
@login_required
def new(compound_id):
    """
        Create page for peaks, only accessible for logged in users

    Args:
        compound_id (int): id of the compound to create a peak spectrum for

    Returns:
        if a peak spectrum already exists for the given compound, redirects to the show page of the compound with error message
        otherwise, renders the page for creating a new peak spectrum
    """
    # check if peak spectrum already exists
    if peak_exists(compound_id):
        return redirect(url_for('compounds.show', compound_id=compound_id))

    # get the wavenumbers and the plot for the user to label
    wavenumbers, img, _ = get_wavenumbers_and_img(compound_id)

    # get all intensity choices from the database
    intensity_choices = db.session.query(Intensity).all()

    # create the form
    form = PeakForm()
    return render_template('resources/peaks/new.html', form=form, compound_id=compound_id, plot=img,
                           wavenumbers=wavenumbers,
                           intensities=intensity_choices)


def get_form_data(form):
    """
        Gets the intensity-classification of every peak from the form and returns it as a dictionary

    Args:
        form (request.form): a dictionary-like object containing the form data

    Returns:
        data (dict): a dictionary with the wavenumber as key and the intensity-classification as value
    """
    # get evey key-value pair from the form where the key contains '_intensity'
    data = {float(k.rstrip("_intensity")): v for k, v in form.items() if '_intensity' in k}
    return data


def create_spectrum_and_peaks(compound_id, data):
    """
        Creates a peak spectrum (csv and png) for the given compound, creates peaks which link the wavenumbers of the spectrum to the intensity

    Args:
        compound_id (int): id of the compound to create a peak spectrum for
        data (dict): key-value pairs of the wavenumber and the intensity-classification

    Returns:
        None
    """
    # create the peak spectrum and plot
    spectrum_type_peak = 3
    wavenumbers, img, filepath = get_wavenumbers_and_img(compound_id)
    filepath = filepath.replace('.csv', '_peaks.csv')
    # store peaks_array in dataframe and save as csv
    peaks_df = pd.DataFrame(wavenumbers, columns=['Wavenumber', 'Intensity'])
    peaks_df.to_csv(filepath, index=False)

    # store image
    with open(filepath.replace('.csv', '.png'), 'wb') as f:
        f.write(base64.b64decode(img))

    # create the peak spectrum
    spectrum_type_peak = 3

    peak_spectrum = Spectrum(file_path=filepath, compound_id=compound_id, spectrum_type_id=spectrum_type_peak)
    db.session.add(peak_spectrum)
    db.session.commit()

    # get the id of the peak spectrum
    peak_spectrum_id = db.session.query(Spectrum).filter(Spectrum.compound_id == compound_id).filter(
        Spectrum.spectrum_type_id == spectrum_type_peak).first().id

    # create the peaks
    for e in data:
        peak = Peak(spectrum_id=peak_spectrum_id, wavenumber=e, intensity_id=data[e])
        db.session.add(peak)
    db.session.commit()


@bp.route('/new/<compound_id>', methods=['POST'])
@login_required
def new_post(compound_id):
    """
        Creates a new peak spectrum for the given compound, only accessible for logged in users

    Args:
        compound_id (int): id of the compound to create a peak spectrum for

    Returns:
        redirects to the show page of the compound with a flash message based on the success of the deletion
        no form validation, because the form is created dynamically and each wavenumber
        is classified with the first intensity available by default and no field can be empty
    """
    # check if peak spectrum already exists
    if peak_exists(compound_id):
        return redirect(url_for('compounds.show', compound_id=compound_id))

    # read the form data
    data = get_form_data(request.form)
    try:
        create_spectrum_and_peaks(compound_id, data)
        flash('Peak-Spektrum wurde erstellt', 'success')
        return redirect(url_for('compounds.show', compound_id=compound_id))
    except:
        flash('Es ist ein Fehler aufgetreten', 'danger')
        return redirect(url_for('compounds.show', compound_id=compound_id))


@bp.route('/edit/<spectrum_id>', methods=['GET'])
@login_required
def edit(spectrum_id):
    """
        Edit page for peaks, only accessible for logged in users

    Args:
        spectrum_id (int): id of the spectrum which links the peaks to be edited

    Returns:
        rendered template of the edit page, with the form for editing the peaks
    """
    # get all peaks of the spectrum
    peaks = db.session.query(Peak).filter(Peak.spectrum_id == spectrum_id).all()
    form = PeakForm()
    intensity_choices = db.session.query(Intensity).all()
    compound_id = db.session.query(Spectrum).filter(Spectrum.id == spectrum_id).first().compound_id
    image_path = db.session.query(Spectrum).filter(Spectrum.id == spectrum_id).first().file_path.replace('.csv', '.png')
    plot = None
    with open(image_path, 'rb') as f:
        plot= base64.b64encode(f.read()).lstrip(b'\n').decode('utf-8')
    return render_template('resources/peaks/edit.html', form=form, peaks=peaks, intensities=intensity_choices,
                           compound_id=compound_id, plot=plot)


@bp.route('/edit/<spectrum_id>', methods=['POST'])
@login_required
def edit_post(spectrum_id):
    """
        Edits the peaks corresponding to a peak spectrum, only accessible for logged in users

    Args:
        spectrum_id (int): id of the spectrum which links the peaks to be edited

    Returns:
        redirects to the show page of the compound with a flash message based on the success of the deletion
        no form validation, because each wavenumber is already classified with an intensity and no field can be empty

    """
    # read the form data
    data = get_form_data(request.form)
    try:
        peaks = db.session.query(Peak).filter(Peak.spectrum_id == spectrum_id).all()
        for i, e in enumerate(peaks):
            peaks[i].intensity_id = data[e.wavenumber]
        db.session.commit()
        flash('Peak-Spektrum wurde aktualisiert', 'success')
        return redirect(url_for('compounds.show', compound_id=db.session.query(Spectrum).filter(Spectrum.id == spectrum_id).first().compound_id))
    except:
        flash('Es ist ein Fehler aufgetreten', 'danger')
        return redirect(url_for('compounds.show', compound_id=db.session.query(Spectrum).filter(Spectrum.id == spectrum_id).first().compound_id))