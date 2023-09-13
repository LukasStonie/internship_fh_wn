import sqlalchemy.exc
from flask import render_template, request, url_for, flash, redirect
from flask_login import login_required, current_user

from app.forms.forms import CompoundsForm
from app.routes.compounds import bp
from app.models.model import Compound, Lens, Laser, SpectralRange, Resolution, Aperture, Slide, Substrate, Spectrum, \
    SpectrumType, PreprocessingSteps
from app.extensions import db
from datetime import date
import base64


@bp.route('/')
@login_required
def index():
    compounds = db.session.query(Compound).all()
    return render_template('resources/compounds/index.html', compounds=compounds)


@bp.route('/new', methods=['GET'])
@login_required
def new():
    form = build_compound_form()
    return render_template('resources/compounds/new.html', form=form)


@bp.route('/new', methods=['POST'])
@login_required
def new_post():
    # convert request.form to form object
    # form = CompoundsForm(request.form)
    form = build_compound_form()
    form.name.data = request.form['name']
    form.coaddition.data = request.form['coaddition']
    form.integration_time.data = request.form['integration_time']
    form.laser_power.data = request.form['laser_power']
    form.description.data = request.form['description']
    # if the form is not valid, redirect to the new page and pass the values from the form
    if not form.validate():
        return render_template('resources/compounds/new.html', form=form)
    # if the form is valid, create a new slide and redirect to the index page
    else:
        # if unique constraint is violated, inform the user
        try:
            compound = Compound(name=form.name.data, coaddition=form.coaddition.data,
                                integration_time=form.integration_time.data,
                                lens_id=form.lenses.data, laser_id=form.lasers.data, laser_power=form.laser_power.data,
                                spectral_range_id=form.spectral_ranges.data, resolution_id=form.resolutions.data,
                                aperture_id=form.apertures.data, slide_id=form.slides.data)
            if form.substrates.data != 'None':
                compound.substrate_id = form.substrates.data
            if form.description.data != '':
                compound.description = form.description.data

            compound.date = date.today().strftime("%d.%m.%Y")
            compound.user = current_user.email
            db.session.add(compound)
            db.session.commit()

            if form.create.data:
                return redirect(url_for('compounds.index'))
            elif form.create_and_add.data:
                return redirect(url_for('spectra.new', compound_id=compound.id))
        except sqlalchemy.exc.IntegrityError:
            flash('Diese Bezeichnung existiert bereits', 'danger')
            return render_template('resources/compounds/new.html', form=form)


@bp.route('/<compound_id>/edit', methods=['GET'])
@login_required
def edit(compound_id):
    compound = db.session.query(Compound).filter(Compound.id == compound_id).first()
    form = build_compound_form()
    form.name.data = compound.name
    form.coaddition.data = compound.coaddition
    form.integration_time.data = compound.integration_time
    form.laser_power.data = compound.laser_power
    form.lenses.data = str(compound.lens_id)
    form.lasers.data = str(compound.laser_id)
    form.spectral_ranges.data = str(compound.spectral_range_id)
    form.resolutions.data = str(compound.resolution_id)
    form.apertures.data = str(compound.aperture_id)
    form.slides.data = str(compound.slide_id)
    form.description.data = compound.description

    if compound.substrate_id is not None:
        form.substrates.data = str(compound.substrate_id)
    else:
        form.substrates.default = 'None'

    return render_template('resources/compounds/edit.html', form=form)


@bp.route('/<compound_id>/edit', methods=['POST'])
@login_required
def edit_post(compound_id):
    # convert request.form to form object

    form = CompoundsForm(request.form)

    # if the form is not valid, redirect to the new page and pass the values from the form
    if not form.validate():
        return render_template('resources/compounds/edit.html', form=form)

    # if the form is valid, create a new slide and redirect to the index page
    else:
        # if unique constraint is violated, inform the user
        try:
            compound = db.session.query(Compound).filter(Compound.id == compound_id).first()
            compound.name = form.name.data
            compound.coaddition = form.coaddition.data
            compound.integration_time = form.integration_time.data
            compound.lens_id = form.lenses.data
            compound.laser_id = form.lasers.data
            compound.laser_power = form.laser_power.data
            compound.spectral_range_id = form.spectral_ranges.data
            compound.resolution_id = form.resolutions.data
            compound.aperture_id = form.apertures.data
            compound.slide_id = form.slides.data

            if form.substrates.data != 'None':
                compound.substrate_id = form.substrates.data
            if form.description.data != '':
                compound.description = form.description.data

            db.session.add(compound)
            db.session.commit()
            return redirect(url_for('compounds.index'))
        except sqlalchemy.exc.IntegrityError:
            flash('Diese Bezeichnung existiert bereits', 'danger')
            return render_template('resources/compounds/edit.html', form=form)


@bp.route('/<compound_id>/delete')
@login_required
def delete(compound_id):
    compound = db.session.query(Compound).filter(Compound.id == compound_id).first()
    db.session.delete(compound)
    db.session.commit()
    flash("Substanz wurde gelöscht", 'success')
    return redirect(url_for('compounds.index'))


@bp.route('/<compound_id>/show')
@login_required
def show(compound_id):
    compound = db.session.query(Compound).filter(Compound.id == compound_id).first()
    lookup = {
        'lens': db.session.query(Lens).filter(Lens.id == compound.lens_id).first(),
        'laser': db.session.query(Laser).filter(Laser.id == compound.laser_id).first(),
        'spectral_range': db.session.query(SpectralRange).filter(
            SpectralRange.id == compound.spectral_range_id).first(),
        'resolution': db.session.query(Resolution).filter(Resolution.id == compound.resolution_id).first(),
        'aperture': db.session.query(Aperture).filter(Aperture.id == compound.aperture_id).first(),
        'slide': db.session.query(Slide).filter(Slide.id == compound.slide_id).first(),
        'substrate': db.session.query(Substrate).filter(Substrate.id == compound.substrate_id).first(),
        'spectra_type': db.session.query(SpectrumType).all(),
        'preprocessing_steps': db.session.query(PreprocessingSteps).all()
    }
    spectra = db.session.query(Spectrum).filter(Spectrum.compound_id == compound_id).all()
    for i in spectra:
        print(i.preprocessing_steps)
    plots = {}
    for i in spectra:
        image_path = i.file_path.replace('csv', 'png')
        with open(image_path, 'rb') as f:
            plots[i.id] = base64.b64encode(f.read()).lstrip(b'\n').decode('utf-8')

    return render_template('resources/compounds/show.html', compound=compound, lookup=lookup, spectra=spectra,
                           plots=plots)


def build_compound_form():
    lenses = db.session.query(Lens).all()
    lasers = db.session.query(Laser).all()
    spectral_ranges = db.session.query(SpectralRange).all()
    resolutions = db.session.query(Resolution).all()
    apertures = db.session.query(Aperture).all()
    slides = db.session.query(Slide).all()
    substrates = db.session.query(Substrate).all()

    form = CompoundsForm()
    form.lenses.choices = [(lens.id, str(lens.zoom) + "x, " + str(lens.numerical_aperture)) for lens in lenses]
    form.lasers.choices = [(laser.id, str(laser.wavelength)) for laser in lasers]
    form.spectral_ranges.choices = [(spectral_range.id, str(spectral_range.start) + " - " + str(spectral_range.end)) for
                                    spectral_range in spectral_ranges]
    form.resolutions.choices = [(resolution.id, resolution.description) for resolution in resolutions]
    form.apertures.choices = [(aperture.id, aperture.size) for aperture in apertures]
    form.slides.choices = [(slide.id, slide.name) for slide in slides]

    # need to add option for no substrate
    form.substrates.choices = [(None, 'Keines')]
    substrates = [(substrate.id, substrate.name) for substrate in substrates]
    for i in substrates:
        form.substrates.choices.append(i)

    return form
