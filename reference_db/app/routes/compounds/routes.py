import sqlalchemy.exc
from flask import render_template, request, url_for, flash, redirect
from app.routes.compounds import bp
from app.models.model import Compound, Lens, Laser, SpectralRange, Resolution, Aperture, Slide, Substrate, Spectrum
from app.extensions import db
from datetime import date


def validate_form(form):
    # check if the form is valid
    form_ok = True
    # check every field if it is empty
    # set form_ok to False if any field is empty
    if not form['name']:
        flash('Bezeichnung ist ein Pflichtfeld', 'error')
        form_ok = False
    if not form['coaddition']:
        flash('Koaddition ist ein Pflichtfeld', 'error')
        form_ok = False
    if not form['integration_time']:
        flash('Integrationszeit ist ein Pflichtfeld', 'error')
        form_ok = False
    if not form['lens_id']:
        flash('Linse ist ein Pflichtfeld', 'error')
        form_ok = False
    if not form['laser_id']:
        flash('Laser ist ein Pflichtfeld', 'error')
        form_ok = False
    if not form['laser_power']:
        flash('Laserleistung ist ein Pflichtfeld', 'error')
        form_ok = False
    if not form['spectral_range_id']:
        flash('Spektralbereich ist ein Pflichtfeld', 'error')
        form_ok = False
    if not form['resolution_id']:
        flash('Auflösung ist ein Pflichtfeld', 'error')
        form_ok = False
    if not form['aperture_id']:
        flash('Blende ist ein Pflichtfeld', 'error')
        form_ok = False
    if not form['slide_id']:
        flash('Objektträger ist ein Pflichtfeld', 'error')
        form_ok = False

    # return whether form is valid
    # return the values from the form for new compound or redirect
    return form_ok, form['name'], \
        form['coaddition'], form['integration_time'], \
        form['lens_id'], form['laser_id'], \
        form['laser_power'], form['spectral_range_id'], \
        form['resolution_id'], form['aperture_id'], \
        form['slide_id']


@bp.route('/')
def index():
    compounds = db.session.query(Compound).all()
    return render_template('resources/compounds/index.html', compounds=compounds)


@bp.route('/new', methods=['GET', 'POST'])
def new():
    # if the request method is POST, the form was submitted
    # validate the form and create a new slide
    if request.method == 'POST':
        # validate form
        # form_ok signifies if the form is valid or not
        # name is the value from the form
        form_ok, name, coaddition, integration_time, \
            lens_id, laser_id, laser_power, \
            spectral_range_id, resolution_id, \
            aperture_id, slide_id = validate_form(request.form)
        # if the form is not valid, redirect to the new page and pass the values from the form
        if not form_ok:
            return redirect(
                url_for('compounds.new', name=name, coaddition=coaddition,
                        integration_time=integration_time, lens_id=lens_id,
                        laser_id=laser_id, laser_power=laser_power,
                        spectral_range_id=spectral_range_id,
                        resolution_id=resolution_id, aperture_id=aperture_id,
                        slide_id=slide_id,
                        substrate_id=request.form['substrate_id'] if request.form['substrate_id'] else None,
                        description=request.form['description'] if request.form['description'] else None))
        # if the form is valid, create a new slide and redirect to the index page
        else:
            # if unique constraint is violated, inform the user
            try:
                compound = Compound(name=name, coaddition=coaddition, integration_time=integration_time,
                                    lens_id=lens_id, laser_id=laser_id, laser_power=laser_power,
                                    spectral_range_id=spectral_range_id, resolution_id=resolution_id,
                                    aperture_id=aperture_id, slide_id=slide_id)
                if request.form['substrate_id'] is not None:
                    compound.substrate_id = request.form['substrate_id']
                if request.form['description'] is not None:
                    compound.description = request.form['description']
                compound.date = date.today().strftime("%d.%m.%Y")
                compound.user = 'admin'  # TODO: get user from session
                db.session.add(compound)
                db.session.commit()
                return redirect(url_for('compounds.index'))
            except sqlalchemy.exc.IntegrityError:
                flash('Diese Bezeichnung existiert bereits', 'error')
                return redirect(
                    url_for('compounds.new', name=name, coaddition=coaddition,
                            integration_time=integration_time, lens_id=lens_id,
                            laser_id=laser_id, laser_power=laser_power,
                            spectral_range_id=spectral_range_id,
                            resolution_id=resolution_id, aperture_id=aperture_id,
                            slide_id=slide_id,
                            substrate_id=request.form['substrate_id'] if request.form['substrate_id'] else None,
                            description=request.form['description'] if request.form['description'] else None))
    # if the request method is GET, the user wants to display the form
    else:
        lenses = db.session.query(Lens).all()
        lasers = db.session.query(Laser).all()
        spectral_ranges = db.session.query(SpectralRange).all()
        resolutions = db.session.query(Resolution).all()
        apertures = db.session.query(Aperture).all()
        slides = db.session.query(Slide).all()
        substrates = db.session.query(Substrate).all()
        lookup = {'lenses': lenses, 'lasers': lasers, 'spectral_ranges': spectral_ranges,
                  'resolutions': resolutions, 'apertures': apertures, 'slides': slides, 'substrates': substrates}
        print(request.args)
        return render_template('resources/compounds/new.html', values=request.args, lookup=lookup)


@bp.route('/<compound_id>/edit', methods=['GET', 'POST'])
def edit(compound_id):
    # if the request method is POST, the form was submitted
    # validate the form and create a new slide
    if request.method == 'POST':
        # validate form
        # form_ok signifies if the form is valid or not
        # name is the value from the form
        form_ok, name, coaddition, integration_time, \
            lens_id, laser_id, laser_power, \
            spectral_range_id, resolution_id, \
            aperture_id, slide_id = validate_form(request.form)
        # if the form is not valid, redirect to the new page and pass the values from the form
        if not form_ok:
            return redirect(
                url_for('compounds.new', name=name, coaddition=coaddition,
                        integration_time=integration_time, lens_id=lens_id,
                        laser_id=laser_id, laser_power=laser_power,
                        spectral_range_id=spectral_range_id,
                        resolution_id=resolution_id, aperture_id=aperture_id,
                        slide_id=slide_id,
                        substrate_id=request.form['substrate_id'] if request.form['substrate_id'] else None,
                        description=request.form['description'] if request.form['description'] else None))
        # if the form is valid, create a new slide and redirect to the index page
        else:
            # if unique constraint is violated, inform the user
            try:
                compound = db.session.query(Compound).filter(Compound.id == compound_id).first()
                compound.name = name
                compound.coaddition = coaddition
                compound.integration_time = integration_time
                compound.lens_id = lens_id
                compound.laser_id = laser_id
                compound.laser_power = laser_power
                compound.spectral_range_id = spectral_range_id
                compound.resolution_id = resolution_id
                compound.aperture_id = aperture_id
                compound.slide_id = slide_id

               # if request.form['substrate_id']:
                compound.substrate_id = request.form['substrate_id']
               # if request.form['description']:
                compound.description = request.form['description']
                db.session.add(compound)
                db.session.commit()
                return redirect(url_for('compounds.index'))
            except sqlalchemy.exc.IntegrityError:
                flash('Diese Bezeichnung existiert bereits', 'error')
                return redirect(
                    url_for('compounds.edit', compound_id=compound_id, name=name, coaddition=coaddition,
                            integration_time=integration_time, lens_id=lens_id,
                            laser_id=laser_id, laser_power=laser_power,
                            spectral_range_id=spectral_range_id,
                            resolution_id=resolution_id, aperture_id=aperture_id,
                            slide_id=slide_id,
                            substrate_id=request.form['substrate_id'] if request.form['substrate_id'] else None,
                            description=request.form['description'] if request.form['description'] else None))
    # if the request method is GET, the user wants to display the form
    else:
        len_args = len(request.args.keys())
        compound = \
            vars(db.session.query(Compound).filter(Compound.id == compound_id).first()) \
                if len_args == 0 \
                else request.args
        lenses = db.session.query(Lens).all()
        lasers = db.session.query(Laser).all()
        spectral_ranges = db.session.query(SpectralRange).all()
        resolutions = db.session.query(Resolution).all()
        apertures = db.session.query(Aperture).all()
        slides = db.session.query(Slide).all()
        substrates = db.session.query(Substrate).all()
        lookup = {'lenses': lenses, 'lasers': lasers, 'spectral_ranges': spectral_ranges,
                  'resolutions': resolutions, 'apertures': apertures, 'slides': slides, 'substrates': substrates}

        return render_template('resources/compounds/edit.html', compound=compound, lookup=lookup)


@bp.route('/<compound_id>/delete')
def delete(compound_id):
    compound = db.session.query(Compound).filter(Compound.id == compound_id).first()
    db.session.delete(compound)
    db.session.commit()
    return redirect(url_for('compounds.index'))


@bp.route('/<compound_id>/show')
def show(compound_id):
    compound = db.session.query(Compound).filter(Compound.id == compound_id).first()
    lookup = {
        'lens': db.session.query(Lens).filter(Lens.id  == compound.lens_id).first(),
        'laser': db.session.query(Laser).filter(Laser.id  == compound.laser_id).first(),
        'spectral_range': db.session.query(SpectralRange).filter(SpectralRange.id  == compound.spectral_range_id).first(),
        'resolution': db.session.query(Resolution).filter(Resolution.id  == compound.resolution_id).first(),
        'aperture': db.session.query(Aperture).filter(Aperture.id  == compound.aperture_id).first(),
        'slide': db.session.query(Slide).filter(Slide.id  == compound.slide_id).first(),
        'substrate': db.session.query(Substrate).filter(Substrate.id  == compound.substrate_id).first()
    }
    spectra = db.session.query(Spectrum).filter(Spectrum.compound_id == compound_id).all()
    return render_template('resources/compounds/show.html', compound=compound, lookup=lookup, spectra=spectra)
