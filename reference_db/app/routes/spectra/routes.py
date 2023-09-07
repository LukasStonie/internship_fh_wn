import os.path
from io import BytesIO
import sqlalchemy.exc
from flask import render_template, request, url_for, flash, redirect, send_file

from config import Config
from app.routes.spectra import bp
from app.models.model import Spectrum, SpectrumType, PreprocessingSteps
from app.extensions import db
from app.extensions import convert
from app.extensions import plt


def validate_form(request):
    # check if the form is valid
    form_ok = True

    # check every field if it is empty
    # set form_ok to False if any field is empty
    if not request.files['spectrum']:
        flash('Bitte fügen Sie ein Spektrum hinzu', 'danger')
        form_ok = False
    if not request.form['spectrum_type_id']:
        flash('Bitte wählen Sie einen Spektrumtyp aus', 'danger')
        form_ok = False
    if request.form['spectrum_type_id'] == '2' and not request.form.getlist('step_check'):
        flash('Bitte wählen Sie mindestens eine Vorverarbeitung aus', 'danger')
        form_ok = False
    return form_ok, int(request.form['spectrum_type_id']), [int(x) for x in request.form.getlist('step_check')]


def read_file_and_save(file, compound_id, spectrum_type_id, preprocessing_step_ids: list):
    # read the file via raman_pca load_data and convert to pd.Dataframe
    spectral_data = convert.spectrum_to_df(file)

    # create a string of the preprocessing_step_ids
    preprocessing_steps = ""
    if len(preprocessing_step_ids) != 0:
        for preprocessing_step_id in preprocessing_step_ids:
            preprocessing_steps += str(preprocessing_step_id) + '_'
        preprocessing_steps = preprocessing_steps[:-1]
    else:
        preprocessing_steps = "raw"
    # create the path to the directory where the file should be stored
    dir_path = os.path.join(Config.APPDATA_PATH, 'compounds', str(compound_id), 'spectra', str(spectrum_type_id))
    # create the directory if it does not exist
    os.makedirs(dir_path, exist_ok=True)
    # create the path to the file
    file_path = os.path.join(dir_path, preprocessing_steps + '.csv')
    # store dataframe in filesystem accordingly
    # appdata/compounds/<compound_id>/spectra/<spectrum_type_id>/<preprocessing_step_ids>.csv
    spectral_data.to_csv(file_path, index=False)

    # create a plot of the spectrum
    plt.plot(spectral_data.iloc[:, 0], spectral_data.iloc[:, 1])
    plt.xlabel('Wavenumber (cm^-1)')
    plt.ylabel('Intensity (-)')
    plt.savefig(os.path.join(dir_path, preprocessing_steps + '.png'))
    # return the path to the file
    return file_path


@bp.route('/new/<compound_id>', methods=['GET', 'POST'])
def new(compound_id):
    # if the request method is POST, the form was submitted
    # validate the form and create a new slide
    if request.method == 'POST':
        print(request.form)
        print(request.files)
        # check if the form is valid
        form_ok, spectrum_type_id, preprocessing_step_ids = validate_form(request)
        print(preprocessing_step_ids)
        if not form_ok:
            return redirect(url_for('spectra.new',
                                    compound_id=compound_id,
                                    spectrum_type_id=spectrum_type_id,
                                    preprocessing_step_ids=preprocessing_step_ids))

        try:
            path = ""
            spectrum = None
            if spectrum_type_id == 1:
                path = read_file_and_save(request.files['spectrum'], compound_id,
                                          spectrum_type_id, [])
                spectrum = Spectrum(file_path=path, compound_id=compound_id, spectrum_type_id=spectrum_type_id)
            elif spectrum_type_id == 2:
                path = read_file_and_save(request.files['spectrum'], compound_id,
                                          spectrum_type_id, preprocessing_step_ids)
                preprocessing_steps = db.session.query(PreprocessingSteps).filter(
                    PreprocessingSteps.id.in_(preprocessing_step_ids)).all()
                spectrum = Spectrum(file_path=path, compound_id=compound_id, spectrum_type_id=spectrum_type_id,
                                    preprocessing_steps=preprocessing_steps)

            db.session.add(spectrum)
            db.session.commit()
            flash('Spektrum erfolgreich hinzugefügt', 'success')
            return redirect(url_for('compounds.show', compound_id=compound_id))
        except sqlalchemy.exc.IntegrityError as e:
            print(e)
            flash('Spektrum konnte nicht hinzugefügt werden, da der Dateipfad schon existiert', 'danger')
            return redirect(url_for('spectra.new', compound_id=compound_id))
        except Exception as e:
            print(e)
            flash(
                'Datei konnte nicht gelesen werden. Bitte überprüfen Sie die Datei und konverterieren Sie sie gegebenenfalls in das CSV Format',
                'danger')
            return redirect(url_for('spectra.new', compound_id=compound_id))


    # if the request method is GET, the user wants to display the form
    else:
        preprocessing_steps = db.session.query(PreprocessingSteps).all()
        spectrum_types = db.session.query(SpectrumType).all()
        lookup = {
            'preprocessing_steps': preprocessing_steps,
            'spectrum_types': spectrum_types
        }
        print(lookup)
        return render_template('resources/spectra/new.html', values=request.args, lookup=lookup, compound_id=compound_id)


@bp.route('/download/<spectrum_id>')
def download(spectrum_id):
    spectrum = db.session.query(Spectrum).filter(Spectrum.id == spectrum_id).first()
    return send_file(spectrum.file_path, as_attachment=True)