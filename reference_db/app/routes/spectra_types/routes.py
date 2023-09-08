import sqlalchemy.exc
from flask import render_template, request, url_for, flash, redirect
from flask_login import login_required

from app.forms.forms import SpectralTypesForm
from app.routes.spectra_types import bp
from app.models.model import SpectrumType
from app.extensions import db


@bp.route('/')
@login_required
def index():
    spectra_types = db.session.query(SpectrumType).all()
    return render_template('resources/spectra_types/index.html', spectra_types=spectra_types)


@bp.route('/new', methods=['GET'])
@login_required
def new():
    form = SpectralTypesForm()
    return render_template('resources/spectra_types/new.html', form=form)


@bp.route('/new', methods=['POST'])
@login_required
def new_post():
    # convert request.form to a form object
    form = SpectralTypesForm(request.form)
    # if the form is not valid, redirect to the new page and pass the values from the form
    if not form.validate():
        return render_template('resources/spectra_types/new.html', form=form)
    # if the form is valid, create a new slide and redirect to the index page
    else:
        # if unique constraint is violated, inform the user
        try:
            spectrum_type = SpectrumType(name=form.description.data)
            db.session.add(spectrum_type)
            db.session.commit()
            return redirect(url_for('spectra_types.index'))
        except sqlalchemy.exc.IntegrityError:
            flash('Diese Bezeichnung existiert bereits', 'error')
            return render_template('resources/spectra_types/new.html', form=form)


@bp.route('/<spectrum_type_id>/edit', methods=['GET'])
@login_required
def edit(spectrum_type_id):
    spectrum_type = db.session.query(SpectrumType).filter(SpectrumType.id == spectrum_type_id).first()
    form = SpectralTypesForm()
    form.description.data = spectrum_type.name
    return render_template('resources/spectra_types/edit.html', form=form)


@bp.route('/<spectrum_type_id>/edit', methods=['POST'])
@login_required
def edit_post(spectrum_type_id):
    # convert request.form to a form object
    form = SpectralTypesForm(request.form)
    # if the form is not valid, redirect to the new page and pass the values from the form
    if not form.validate():
        return render_template('resources/spectra_types/edit.html', form=form)
    # if the form is valid, create a new slide and redirect to the index page
    else:
        # if unique constraint is violated, inform the user
        try:
            spectrum_type = db.session.query(SpectrumType).filter_by(id=spectrum_type_id).one()
            spectrum_type.name = form.description.data
            db.session.commit()
            return redirect(url_for('spectra_types.index'))
        except sqlalchemy.exc.IntegrityError:
            flash('Diese Bezeichnung existiert bereits', 'error')
            return render_template('resources/spectra_types/edit.html', form=form)


@bp.route('/<spectrum_type_id>/delete')
@login_required
def delete(spectrum_type_id):
    spectrum_type = db.session.query(SpectrumType).filter(SpectrumType.id == spectrum_type_id).first()
    db.session.delete(spectrum_type)
    db.session.commit()
    return redirect(url_for('spectra_types.index'))
