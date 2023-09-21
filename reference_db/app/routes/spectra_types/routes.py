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
    """
        Index page for spectra_types, only accessible for logged in users. Allowing the the user to add, edit and delete spectra_types

    Returns:
        rendered template of the index page, with all the spectra_types
    """
    spectra_types = db.session.query(SpectrumType).all()
    return render_template('resources/spectra_types/index.html', spectra_types=spectra_types)


@bp.route('/new', methods=['GET'])
@login_required
def new():
    """
        Create page for spectra_types, only accessible for logged in users

    Returns:
        rendered template of the new page, with the form for creating a new spectrum_type
    """
    form = SpectralTypesForm()
    return render_template('resources/spectra_types/new.html', form=form)


@bp.route('/new', methods=['POST'])
@login_required
def new_post():
    """
        Creates a new spectrum_type if form is valid, only accessible for logged in users

    Returns:
        based on the validation of the form, either redirects to this resources index page or
        renders the Create page again with validation errors (WTForms) or integrity errors (SQL constraints)
    """
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
            flash('Diese Bezeichnung existiert bereits', 'danger')
            return render_template('resources/spectra_types/new.html', form=form)


@bp.route('/<spectrum_type_id>/edit', methods=['GET'])
@login_required
def edit(spectrum_type_id):
    """
        Edit page for spectra_types, only accessible for logged in users

    Args:
        spectrum_type_id (int): id of the spectrum_type to be edited

    Returns:
        rendered template of the edit page, with the form for editing the spectrum_type
    """
    # get the spectrum_type to be edited, create the form and set the description to the current value
    spectrum_type = db.session.query(SpectrumType).filter(SpectrumType.id == spectrum_type_id).first()
    form = SpectralTypesForm()
    form.description.data = spectrum_type.name
    return render_template('resources/spectra_types/edit.html', form=form)


@bp.route('/<spectrum_type_id>/edit', methods=['POST'])
@login_required
def edit_post(spectrum_type_id):
    """
        Edits the spectrum_type if form is valid, only accessible for logged in users

    Args:
        spectrum_type_id (int): id of the spectrum_type to be edited

    Returns:
        based on the validation of the form, either redirects to this resources index page or
        renders the Edit page again with validation errors (WTForms) or integrity errors (SQL constraints)
    """
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
            flash('Diese Bezeichnung existiert bereits', 'danger')
            return render_template('resources/spectra_types/edit.html', form=form)


@bp.route('/<spectrum_type_id>/delete')
@login_required
def delete(spectrum_type_id):
    """
        Deletes the spectrum_type if not used in a spectrum, only accessible for logged in users

    Args:
        spectrum_type_id (int): id of the spectrum_type to be deleted

    Returns:
        redirects to the index page with a flash message based on the success of the deletion
    """
    try:
        spectrum_type = db.session.query(SpectrumType).filter(SpectrumType.id == spectrum_type_id).first()
        db.session.delete(spectrum_type)
        db.session.commit()
        flash("Spektrumart wurde gelöscht", 'success')
        return redirect(url_for('spectra_types.index'))
    except sqlalchemy.exc.IntegrityError:
        flash('Diese Spektrumart wird noch verwendet und kann daher nicht gelöscht werden.', 'danger')
        return redirect(url_for('spectra_types.index'))
    except:
        flash('Spektrumart konnte nicht gelöscht werden. Probieren Sie es später erneut.', 'danger')
