import sqlalchemy.exc
from flask import render_template, request, url_for, flash, redirect
from flask_login import login_required

from app.forms.forms import SpectralRangesForm
from app.routes.spectral_ranges import bp
from app.models.model import SpectralRange
from app.extensions import db


@bp.route('/')
@login_required
def index():
    """
        Index page for spectral_ranges, only accessible for logged in users. Allowing the the user to add, edit and delete spectral_ranges

    Returns:
        rendered template of the index page, with all the spectral_ranges
    """
    spectral_ranges = db.session.query(SpectralRange).all()
    return render_template('resources/spectral_ranges/index.html', spectral_ranges=spectral_ranges)


@bp.route('/new', methods=['GET'])
@login_required
def new():
    """
        Create page for spectral_ranges, only accessible for logged in users

    Returns:
        rendered template of the new page, with the form for creating a new spectral_range
    """
    form = SpectralRangesForm()
    return render_template('resources/spectral_ranges/new.html', form=form)


@bp.route('/new', methods=['POST'])
@login_required
def new_post():
    """
        Creates a new spectral_range if form is valid, only accessible for logged in users

    Returns:
        based on the validation of the form, either redirects to this resources index page or
        renders the Create page again with validation errors (WTForms) or integrity errors (SQL constraints)
    """

    # convert request.form to form object
    form = SpectralRangesForm(request.form)
    # if the form is not valid, redirect to the new page and pass the values from the form
    if not form.validate():
        return render_template('resources/spectral_ranges/new.html', form=form)
    # if the form is valid, create a new slide and redirect to the index page
    else:
        # if unique constraint is violated, inform the user
        try:
            spectral_range = SpectralRange(start=form.start.data, end=form.end.data)
            db.session.add(spectral_range)
            db.session.commit()
            return redirect(url_for('spectral_ranges.index'))
        except sqlalchemy.exc.IntegrityError:
            flash('Diese Kombination aus Start und Ende existiert bereits', 'danger')
            return render_template('resources/spectral_ranges/new.html', form=form)


@bp.route('/<spectral_range_id>/edit', methods=['GET'])
@login_required
def edit(spectral_range_id):
    """
        Edit page for spectral_ranges, only accessible for logged in users

    Args:
        spectral_range_id (int): id of the spectral_range to be edited

    Returns:
        rendered template of the edit page, with the form for editing the spectral_range
    """

    # get the spectral_range from the database and populate the form with its values
    spectral_range = db.session.query(SpectralRange).filter(SpectralRange.id == spectral_range_id).first()
    form = SpectralRangesForm(obj=spectral_range)
    return render_template('resources/spectral_ranges/edit.html', form=form)


@bp.route('/<spectral_range_id>/edit', methods=['POST'])
@login_required
def edit_post(spectral_range_id):
    """
        Edits the spectral_range if form is valid, only accessible for logged in users

    Args:
        spectral_range_id (int): id of the spectral_range to be edited

    Returns:
        based on the validation of the form, either redirects to this resources index page or
        renders the Edit page again with validation errors (WTForms) or integrity errors (SQL constraints)
    """
    # convert request.form to form object
    form = SpectralRangesForm(request.form)
    # if the form is not valid, redirect to the new page and pass the values from the form
    if not form.validate():
        return render_template('resources/spectral_ranges/edit.html', form=form)
    # if the form is valid, create a new slide and redirect to the index page
    else:
        # if unique constraint is violated, inform the user
        try:
            spectral_range = db.session.query(SpectralRange).filter(SpectralRange.id == spectral_range_id).first()
            spectral_range.start = form.start.data
            spectral_range.end = form.end.data
            db.session.commit()
            return redirect(url_for('spectral_ranges.index'))
        except sqlalchemy.exc.IntegrityError:
            flash('Diese Kombination aus Start und Ende existiert bereits', 'danger')
            return render_template('resources/spectral_ranges/edit.html', form=form)


@bp.route('/<spectral_range_id>/delete')
@login_required
def delete(spectral_range_id):
    """
        Deletes the spectral_range if not used in a compound, only accessible for logged in users

    Args:
        spectral_range_id (int): id of the spectral_range to be deleted

    Returns:
       redirects to the index page, with a flash message based on the success of the deletion
    """
    try:
        spectral_range = db.session.query(SpectralRange).filter(SpectralRange.id == spectral_range_id).first()
        db.session.delete(spectral_range)
        db.session.commit()
        flash("Spektralbereich wurde gelöscht", 'success')
        return redirect(url_for('spectral_ranges.index'))
    except sqlalchemy.exc.IntegrityError:
        flash('Dieser Spektralbereich wird noch verwendet und konnte daher nicht gelöscht werden', 'danger')
        return redirect(url_for('spectral_ranges.index'))
    except:
        flash("Spektralbereich konnte nicht gelöscht werden. Probieren Sie es später erneut.", 'danger')
        return redirect(url_for('spectral_ranges.index'))
