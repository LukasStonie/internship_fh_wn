from io import BytesIO
import sqlalchemy.exc
from flask import render_template, request, url_for, flash, redirect, send_file
from app.routes.spectra import bp
from app.models.model import Spectrum, SpectrumType, PreprocessingSteps
from app.extensions import db


def validate_form(form):
    return True, form['spectrum_type_id']


def read_file_and_save(file, compound_id, spectrum_id, spectrum_type_id, preprocessing_step_ids):
    # read the file via raman_pca load_data and convert to numpy array
    # store numpy array in filesystem accordingly
    # appdata/compounds/<compound_id>/spectra/<spectrum_type_id>/<preprocessing_step_ids>.csv
    # return the path to the file
    return 'path/to/file'

@bp.route('/new/<compound_id>', methods=['GET', 'POST'])
def new(compound_id):
    # if the request method is POST, the form was submitted
    # validate the form and create a new slide
    if request.method == 'POST':
        selected_preprocessing_steps = [int(x.lstrip('check-')) for x in request.form if x.startswith('check')]
        if request.files['spectrum_processed'] is None:
            flash('Spectrum is a required field', 'error')
            return redirect(url_for('spectra.new', compound_id=compound_id))
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
        return render_template('resources/spectra/new.html', values=request.args, lookup=lookup)
