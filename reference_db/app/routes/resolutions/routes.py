import sqlalchemy.exc
from flask import render_template, request, url_for, flash, redirect
from flask_login import login_required

from app.forms.forms import ResolutionsForm
from app.routes.resolutions import bp
from app.models.model import Resolution
from app.extensions import db


@bp.route('/')
@login_required
def index():
    """
        Index page for resolutions, only accessible for logged in users. Allowing the user to add, edit and delete resolutions
        
    Returns:
        rendered template of the index page, with all the resolutions
        allows the user to add, edit and delete resolutions
    """
    resolutions = db.session.query(Resolution).all()
    return render_template('resources/resolutions/index.html', resolutions=resolutions)


@bp.route('/new', methods=['GET'])
@login_required
def new():
    """
        Create page for resolutions, only accessible for logged in users
        
    Returns:
        rendered template of the new page, with the form for creating a new resolution
    """
    form = ResolutionsForm()
    return render_template('resources/resolutions/new.html', form=form)


@bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_post():
    """
        Creates a new resolution if form is valid, only accessible for logged in users
        
    Returns:
        based on the validation of the form, either redirects to this resources index page or 
        renders the Create page again with validation errors (WTForms) or integrity errors (SQL constraints)
    """
    # convert request.form to a form object
    form = ResolutionsForm(request.form)
    # if the form is not valid, redirect to the new page and pass the values from the form
    if not form.validate():
        return render_template('resources/resolutions/new.html', form=form)
    # if the form is valid, create a new slide and redirect to the index page
    else:
        # if unique constraint is violated, inform the user
        try:
            resolution = Resolution(description=form.description.data)
            db.session.add(resolution)
            db.session.commit()
            return redirect(url_for('resolutions.index'))
        except sqlalchemy.exc.IntegrityError:
            flash('Diese Bezeichnung existiert bereits', 'danger')
            return render_template('resources/resolutions/new.html', form=form)


@bp.route('/<resolution_id>/edit', methods=['GET'])
@login_required
def edit(resolution_id):
    """
        Edit page for resolutions, only accessible for logged in users
        
    Args:
        resolution_id (int): id of the resolution to be edited

    Returns:
        rendered template of the edit page, with the form for editing a resolution
    """
    resolution = db.session.query(Resolution).filter_by(id=resolution_id).first()
    form = ResolutionsForm(obj=resolution)
    return render_template('resources/resolutions/edit.html', form=form)


@bp.route('/<resolution_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(resolution_id):
    """
        Edits the resolution if form is valid, only accessible for logged in users
        
    Args:
        resolution_id (int): id of the resolution to be edited

    Returns:
        based on the validation of the form, either redirects to this resources index page or 
        renders the Edit page again with validation errors (WTForms) or integrity errors (SQL constraints)
    """
    # convert request.form to a form object
    form = ResolutionsForm(request.form)
    # if the form is not valid, redirect to the new page and pass the values from the form
    if not form.validate():
        return render_template('resources/resolutions/edit.html', form=form)
    # if the form is valid, create a new slide and redirect to the index page
    else:
        # if unique constraint is violated, inform the user
        try:
            resolution = db.session.query(Resolution).filter_by(id=resolution_id).first()
            resolution.description = form.description.data
            db.session.commit()
            return redirect(url_for('resolutions.index'))
        except sqlalchemy.exc.IntegrityError:
            flash('Diese Bezeichnung existiert bereits', 'danger')
            return render_template('resources/resolutions/edit.html', form=form)


@bp.route('/<resolution_id>/delete', methods=['GET', 'POST'])
@login_required
def delete(resolution_id):
    """
        Deletes the resolution if not used in a compound, only accessible for logged in users
        
    Args:
        resolution_id (int): id of the resolution to be deleted

    Returns:
        redirects to the index page with a flash message based on the success of the deletion
    """
    try:
        resolution = db.session.query(Resolution).filter_by(id=resolution_id).first()
        db.session.delete(resolution)
        db.session.commit()
        flash("Auflösung wurde gelöscht", 'success')
        return redirect(url_for('resolutions.index'))
    except sqlalchemy.exc.IntegrityError:
        flash('Diese Auflösung wird noch verwendet und kann daher nicht gelöscht werden', 'danger')
        return redirect(url_for('resolutions.index'))
    except:
        flash('Auflösung konnte nicht gelöscht werden. Probieren Sie es später erneut', 'danger')
        return redirect(url_for('resolutions.index'))
