import os.path
from io import BytesIO

import pandas as pd
import sqlalchemy.exc
from flask import render_template, request, url_for, flash, redirect, send_file
from flask_login import login_required

from app.business_logic import convert
from app.external_libs.raman_lib.preprocessing import PeakPicker
from app.forms.forms import SpectraForm, SpectraEditForm
from config import Config
from app.routes.spectra import bp
from app.models.model import Spectrum, SpectrumType, PreprocessingSteps
from app.extensions import db
from scipy.signal import find_peaks
import numpy as np
from app.extensions import plt
import shutil


def build_file_path(compound_id, spectrum_type_id, preprocessing_step_ids: list):
    # create a string of the preprocessing_step_ids
    preprocessing_steps = ""
    if len(preprocessing_step_ids) != 0:
        for preprocessing_step_id in preprocessing_step_ids:
            preprocessing_steps += str(preprocessing_step_id) + '_'
        preprocessing_steps = preprocessing_steps[:-1]
    else:
        preprocessing_steps = "raw"

    # create the path to the directory where the file should be stored
    dir_path = os.path.join(Config.APPDATA_PATH, 'compounds', str(compound_id), 'spectra')
    # create the directory if it does not exist
    os.makedirs(dir_path, exist_ok=True)
    # create the path to the file
    file_name = "type_" + str(spectrum_type_id) + "_steps_" + preprocessing_steps
    file_path = os.path.join(dir_path, file_name + '.csv')

    return file_path


def read_file_and_save(file, compound_id, spectrum_type_id, preprocessing_step_ids: list):
    # read the file via raman_pca load_data and convert to pd.Dataframe
    spectral_data = convert.spectrum_to_df(file)

    file_path = build_file_path(compound_id, spectrum_type_id, preprocessing_step_ids)

    # check if file already exists and raise an error if it does
    if os.path.isfile(file_path):
        raise sqlalchemy.exc.IntegrityError("File already exists", orig=None, params=None)

    # store dataframe in filesystem accordingly
    # appdata/compounds/<compound_id>/spectra/type_<spectrum_type_id>_steps_<preprocessing_step_ids>.csv
    spectral_data.to_csv(file_path, index=False)

    # create a plot of the spectrum
    plt.plot(spectral_data.iloc[:, 0], spectral_data.iloc[:, 1])
    plt.xlabel('Wavenumber ($\mathregular{cm^{-1}}$)')
    plt.ylabel('Intensity (-)')
    plt.savefig(os.path.join(file_path.replace('.csv', '.png')))
    plt.close()

    # return the path to the file
    return file_path


@bp.route('/new/<compound_id>', methods=['GET'])
@login_required
def new(compound_id):
    preprocessing_steps = db.session.query(PreprocessingSteps).all()
    spectrum_types = db.session.query(SpectrumType).all()
    form = SpectraForm()
    form.spectrum_type.choices = [(spectrum_type.id, spectrum_type.name) for spectrum_type in spectrum_types]
    form.preprocessing_steps.choices = [(preprocessing_step.id, preprocessing_step.name) for preprocessing_step in
                                        preprocessing_steps]

    return render_template('resources/spectra/new.html', form=form, compound_id=compound_id)


@bp.route('/new/<compound_id>', methods=['POST'])
def new_post(compound_id):
    # convert request.form to form object
    form = SpectraForm(request.form)
    # get all spectrum types and preprocessing steps and add them to the form
    preprocessing_steps = db.session.query(PreprocessingSteps).all()
    spectrum_types = db.session.query(SpectrumType).all()
    form.spectrum_type.choices = [(spectrum_type.id, spectrum_type.name) for spectrum_type in spectrum_types]
    form.preprocessing_steps.choices = [(preprocessing_step.id, preprocessing_step.name) for preprocessing_step in
                                        preprocessing_steps]
    # get the preprocessing steps from request.form (form object can not handle multiple select fields)
    preprocessing_steps = [int(x) for x in request.form.getlist('step_check')]
    file = request.files['spectrum']
    # check if the form is valid
    if not form.validate() or file.filename == '':
        flash('Bitte füllen Sie alle Felder einschließlich der Datei aus', 'danger')
        return render_template('resources/spectra/new.html', form=form, compound_id=compound_id)

    try:
        path = ""
        spectrum = None
        if int(form.spectrum_type.data) == 1:
            path = read_file_and_save(file, compound_id,
                                      int(form.spectrum_type.data), [])
            spectrum = Spectrum(file_path=path, compound_id=compound_id, spectrum_type_id=int(form.spectrum_type.data))
            spectrum.preprocessing_steps = []
        elif int(form.spectrum_type.data) == 2:
            path = read_file_and_save(file, compound_id,
                                      int(form.spectrum_type.data), preprocessing_steps)
            preprocessing_steps = db.session.query(PreprocessingSteps).filter(
                PreprocessingSteps.id.in_(preprocessing_steps)).all()
            spectrum = Spectrum(file_path=path, compound_id=compound_id, spectrum_type_id=int(form.spectrum_type.data),
                                preprocessing_steps=preprocessing_steps)

        db.session.add(spectrum)
        db.session.commit()
        return redirect(url_for('compounds.show', compound_id=compound_id))
    except sqlalchemy.exc.IntegrityError as e:
        print(e)
        flash('Spektrum konnte nicht hinzugefügt werden, da diese Konfiguration für die Substanz schon existiert',
              'danger')
        return render_template('resources/spectra/new.html', form=form, compound_id=compound_id)
    except Exception as e:
        print(e)
        flash(
            'Datei konnte nicht gelesen werden. Bitte überprüfen Sie die Datei und konverterieren Sie sie gegebenenfalls in das CSV Format',
            'danger')
        return render_template('resources/spectra/new.html', form=form, compound_id=compound_id)


@bp.route('/edit/<spectrum_id>', methods=['GET'])
@login_required
def edit(spectrum_id):
    spectrum = db.session.query(Spectrum).filter(Spectrum.id == spectrum_id).first()
    preprocessing_steps = db.session.query(PreprocessingSteps).all()
    spectrum_types = db.session.query(SpectrumType).all()
    form = SpectraEditForm()
    form.spectrum_type.choices = [(spectrum_type.id, spectrum_type.name) for spectrum_type in spectrum_types]
    form.preprocessing_steps.choices = [(preprocessing_step.id, preprocessing_step.name) for preprocessing_step in
                                        preprocessing_steps]
    form.spectrum_type.data = spectrum.spectrum_type_id
    form.preprocessing_steps.data = [preprocessing_step.id for preprocessing_step in spectrum.preprocessing_steps]
    return render_template('resources/spectra/edit.html', form=form, spectrum=spectrum,
                           compound_id=spectrum.compound_id)


@bp.route('/edit/<spectrum_id>', methods=['POST'])
def edit_post(spectrum_id):
    # get the spectrum from the db
    spectrum = db.session.query(Spectrum).filter(Spectrum.id == spectrum_id).first()
    # convert request.form to form object
    form = SpectraEditForm(request.form)
    # get all spectrum types and preprocessing steps and add them to the form (is somehow empty in the form object)
    preprocessing_steps = db.session.query(PreprocessingSteps).all()
    spectrum_types = db.session.query(SpectrumType).all()
    form.spectrum_type.choices = [(spectrum_type.id, spectrum_type.name) for spectrum_type in spectrum_types]
    form.preprocessing_steps.choices = [(preprocessing_step.id, preprocessing_step.name) for preprocessing_step in
                                        preprocessing_steps]
    # get the preprocessing steps from request.form (form object can not handle multiple select fields)
    preprocessing_step_ids = [int(x) for x in request.form.getlist('step_check')]
    preprocessing_step_ids = preprocessing_step_ids if int(
        form.spectrum_type.data) == 2 else []
    # map the ids to the actual objects for later use
    preprocessing_steps = db.session.query(PreprocessingSteps).filter(
        PreprocessingSteps.id.in_(preprocessing_step_ids)).all()
    # check if the form is valid
    if not form.validate():
        flash('Bitte füllen Sie alle Felder einschließlich der Datei aus', 'danger')
        return render_template('resources/spectra/edit.html', form=form, compound_id=spectrum.compound_id)

    try:
        path = spectrum.file_path
        # build new path
        new_path = build_file_path(spectrum.compound_id, int(form.spectrum_type.data), preprocessing_step_ids)
        # if the file already exists and is not the same file, raise an error
        if os.path.isfile(new_path) and new_path != path:
            raise sqlalchemy.exc.IntegrityError("File already exists", orig=None, params=None)
        # if the user wants to keep the old spectrum, rename the file to fit the new properties
        if not form.new_spectrum.data:
            # rename file to fit new properties --> new_path
            os.rename(path, new_path)
            # rename plot to fit new properties --> new_path
            os.rename(path.replace('.csv', '.png'), new_path.replace('.csv', '.png'))
            path = new_path
        else:
            # get the file from the request
            file = request.files['spectrum']
            # remove old spectrum from filesystem
            remove_spectrum(path)
            # read the file and save it to the filesystem
            path = read_file_and_save(file, spectrum.compound_id,
                                      int(form.spectrum_type.data), preprocessing_step_ids)

        spectrum.file_path = path
        spectrum.spectrum_type_id = int(form.spectrum_type.data)
        spectrum.preprocessing_steps = preprocessing_steps
        db.session.commit()
        return redirect(url_for('compounds.show', compound_id=spectrum.compound_id))
    except sqlalchemy.exc.IntegrityError as e:
        flash('Spektrum konnte nicht hinzugefügt werden, da diese Konfiguration für die Substanz schon existiert',
              'danger')
        return render_template('resources/spectra/edit.html', form=form, compound_id=spectrum.compound_id)
    except Exception as e:
        flash(
            'Datei konnte nicht gelesen werden. Bitte überprüfen Sie die Datei und konverterieren Sie sie gegebenenfalls in das CSV Format',
            'danger')
        return render_template('resources/spectra/edit.html', form=form, compound_id=spectrum.compound_id)


@bp.route('/<spectrum_id>/delete', methods=['GET'])
@login_required
def delete(spectrum_id):
    spectrum = db.session.query(Spectrum).filter(Spectrum.id == spectrum_id).first()
    compound_id = spectrum.compound_id
    remove_spectrum(spectrum.file_path)
    # remove spectrum from db
    db.session.delete(spectrum)
    db.session.commit()
    return redirect(url_for('compounds.show', compound_id=compound_id))


def remove_spectrum(file_path):
    os.remove(file_path)  # remove csv
    os.remove(file_path.replace('.csv', '.png'))  # remove plot
    return


@bp.route('/download/<spectrum_id>')
def download(spectrum_id):
    spectrum = db.session.query(Spectrum).filter(Spectrum.id == spectrum_id).first()
    return send_file(spectrum.file_path, as_attachment=True)


@bp.route('/peaks/<compound_id>')
@login_required
def peaks(compound_id):
    spectrum_type_peak = 3

    # check if peak spectrum already exists
    peak_spectrum = db.session.query(Spectrum).filter(Spectrum.compound_id == compound_id).filter(
        Spectrum.spectrum_type_id == spectrum_type_peak).first()
    if peak_spectrum is not None:
        flash('Es existiert bereits ein Peak-Spektrum für diese Substanz', 'danger')
        return redirect(url_for('compounds.show', compound_id=compound_id))

    # get the spectrum with the highest id
    spectrum = db.session.query(Spectrum).filter(Spectrum.compound_id == compound_id).order_by(
        Spectrum.id.desc()).first()

    # read the spectrum and transpose it -> needed for find_peaks
    data = pd.read_csv(spectrum.file_path, index_col=None).transpose()

    # calculate mean of all spectra and find peaks
    x_mean = data.mean(axis=0)
    peaks = find_peaks(data.iloc[1, :])

    # create empty numpy array with length of data
    # peaks_array = np.full(len(data.iloc[1, :]), min(data.iloc[1, :]))
    peaks_array = np.zeros(data.shape[1])

    # iterate peaks
    for peak in peaks[0]:
        # peak is index in data
        # lookup peak height in data and store in peaks_array
        peaks_array[peak] = data.iloc[1, :][peak]

    combined = np.column_stack((data.iloc[0, :], peaks_array))
    # store peaks_array in dataframe and save as csv
    peaks_df = pd.DataFrame(combined, columns=['Wavenumber', 'Intensity'])
    peaks_df.to_csv(spectrum.file_path.replace('.csv', '_peaks.csv'), index=False)
    # plot peaks_array
    plt.plot(combined[:, 0], combined[:, 1])
    # describe axis
    plt.xlabel('Wavenumber ($\mathregular{cm^{-1}}$)')
    plt.ylabel('Intensity (-)')
    plt.savefig(spectrum.file_path.replace('.csv', '_peaks.png'))
    plt.close()

    spectrum = Spectrum(file_path=spectrum.file_path.replace('.csv', '_peaks.csv'), compound_id=compound_id,
                        spectrum_type_id=spectrum_type_peak)
    db.session.add(spectrum)
    db.session.commit()

    return redirect(url_for('compounds.show', compound_id=compound_id))
