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

from app.forms.forms import PeakForm, WaveNumberIntensityPairForm
from app.routes.peaks import bp

from app.models.model import Peak, Spectrum, Intensity

from app.extensions import db


def peak_exists(compound_id):
    spectrum_type_peak = 3
    # check if peak spectrum already exists
    peak_spectrum = db.session.query(Spectrum).filter(Spectrum.compound_id == compound_id).filter(
        Spectrum.spectrum_type_id == spectrum_type_peak).first()
    if peak_spectrum is not None:
        flash('Es existiert bereits ein Peak-Spektrum für diese Substanz', 'danger')
        return True
    return False


def create_plot(peaks):
    # plot peaks_array
    plt.plot(peaks[:, 0], peaks[:, 1])
    # describe axis
    plt.xlabel('Wavenumber ($\mathregular{cm^{-1}}$)')
    plt.ylabel('Intensity (-)')


def get_wavenumbers_and_img(compound_id):
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

    return wavenumbers, base64.b64encode(img.getvalue()).decode('utf8')


@bp.route('/new/<compound_id>', methods=['GET'])
@login_required
def new(compound_id):
    if peak_exists(compound_id):
        return redirect(url_for('compounds.show', compound_id=compound_id))

    wavenumbers, img = get_wavenumbers_and_img(compound_id)
    print(wavenumbers)
    form = PeakForm()
    # form.wavenumber.data = int(wavenumbers[4])
    # form.intensity.choices = [(i.id, i.description) for i in db.session.query(Intensity).all()]
    # form.wavenumber_intensity_pairs.pop_entry()
    #form.peaks.pop_entry()
    intensities = db.session.query(Intensity).all()
    intensity_choices = [(i.id, i.description) for i in intensities]
    for wn in wavenumbers:
        wni_pair = WaveNumberIntensityPairForm()
        wni_pair.wavenumber.data = int(wn)  # Set default wavenumber
        wni_pair.process()
        form.peaks.append_entry(wni_pair)
        print("wni", wni_pair)
    # print(form.wavenumber_intensity_pairs.entries)
    return render_template('resources/peaks/new.html', form=form, compound_id=compound_id, plot=img, wavenumbers=wavenumbers)
