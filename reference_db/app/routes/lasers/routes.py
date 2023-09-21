import sqlalchemy.exc
from flask import render_template, request, url_for, flash, redirect

from app.forms.forms import LasersForm
from app.routes.lasers import bp
from app.models.model import Laser
from app.extensions import db
from flask_login import login_required, current_user


@bp.route('/')
@login_required
def index():
    """
        Index page for lasers, only accessible for logged in users. Allowing the user to add, edit and delete lasers

    Returns:
        rendered template of the index page, with all the lasers
        allowing the user to add, edit and delete lasers
    """
    lasers = db.session.query(Laser).all()
    return render_template('resources/lasers/index.html', lasers=lasers, name=current_user)


@bp.route('/new', methods=['GET'])
@login_required
def new():
    """
        Create page for lasers, only accessible for logged in users

    Returns:
        rendered template of the new page, with the form for creating a new laser
    """
    form = LasersForm()
    return render_template('resources/lasers/new.html', form=form)


@bp.route('/new', methods=['POST'])
@login_required
def new_post():
    """
        Creates a new laser, only accessible for logged in users

    Returns:
        based on the validation of the form, either redirects to this resources index page or
        renders the Create page again with validation errors (WTForms) or integrity errors (SQL constraints)
    """
    # convert request.form to form object
    form = LasersForm(request.form)
    # if the form is not valid, redirect to the new page and pass the values from the form
    if not form.validate():
        return render_template('resources/lasers/new.html', form=form)
    # if the form is valid, create a new lens and redirect to the index page
    else:
        # if unique constraint is violated, inform the user
        try:
            laser = Laser(wavelength=form.wavelength.data)
            db.session.add(laser)
            db.session.commit()
            return redirect(url_for('lasers.index'))
        except sqlalchemy.exc.IntegrityError:
            flash('Diese Wellenlänge existiert bereits', 'danger')
            return render_template('resources/lasers/new.html', form=form)


@bp.route('/<laser_id>/edit', methods=['GET'])
@login_required
def edit(laser_id):
    """
        Edit page for lasers, only accessible for logged in users

    Args:
        laser_id (int): id of the laser to be edited

    Returns:
        rendered template of the edit page, with the form for editing a laser
    """
    laser = db.session.query(Laser).filter(Laser.id == laser_id).first()
    form = LasersForm(obj=laser)
    return render_template('resources/lasers/edit.html', form=form)


@bp.route('/<laser_id>/edit', methods=['POST'])
@login_required
def edit_post(laser_id):
    """
        Edits the laser, only accessible for logged in users

    Args:
        laser_id (int): id of the laser to be edited

    Returns:
        based on the validation of the form, either redirects to this resources index page or
        renders the Edit page again with validation errors (WTForms) or integrity errors (SQL constraints)
    """
    # convert request.form to form object
    form = LasersForm(request.form)
    # if the form is not valid, redirect to the new page and pass the values from the form
    if not form.validate():
        return render_template('resources/lasers/edit.html', form=form)
        # if the form is valid, create a new lens and redirect to the index page
    else:
        # if unique constraint is violated, inform the user
        try:
            laser = db.session.query(Laser).filter(Laser.id == laser_id).first()
            laser.wavelength = form.wavelength.data
            db.session.commit()
            return redirect(url_for('lasers.index'))
        except sqlalchemy.exc.IntegrityError:
            flash('Diese Wellenlänge existiert bereits', 'danger')
            return render_template('resources/lasers/edit.html', form=form)


@bp.route('/<laser_id>/delete')
@login_required
def delete(laser_id):
    """
        Deletes the laser if not used in a compound, only accessible for logged in users

    Args:
        laser_id (int): id of the laser to be deleted

    Returns:
        redirects to the index page, with a flash message based on the success of the deletion
    """
    try:
        laser = db.session.query(Laser).filter(Laser.id == laser_id).first()
        db.session.delete(laser)
        db.session.commit()
        flash("Laser wurde gelöscht", 'success')
        return redirect(url_for('lasers.index'))
    except sqlalchemy.exc.IntegrityError:
        flash('Dieser Laser wird noch verwendet und kann daher nicht gelöscht werden', 'danger')
        return redirect(url_for('lasers.index'))
    except:
        flash('Laser konnte nicht gelöscht werden. Probieren Sie es später erneut', 'danger')
        return redirect(url_for('lasers.index'))
