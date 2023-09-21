import sqlalchemy.exc
from flask import render_template, request, url_for, flash, redirect
from flask_login import login_required

from app.forms.forms import AperturesForm
from app.routes.apertures import bp
from app.models.model import Aperture
from app.extensions import db


@bp.route('/')
@login_required
def index():
    """
        Index page for apertures, only accessible for logged in users. Allowing the user to add, edit and delete apertures

    Returns:
        rendered template of the index page, with all the apertures
    """
    apertures = db.session.query(Aperture).all()
    return render_template('resources/apertures/index.html', apertures=apertures)


@bp.route('/new', methods=['GET'])
@login_required
def new():
    """
        Create page for apertures, only accessible for logged in users

    Returns:
        rendered template of the new page, with the form for creating a new aperture
    """


    form = AperturesForm()
    return render_template('resources/apertures/new.html', form=form)


@bp.route('/new', methods=['POST'])
@login_required
def new_post():
    """
        Creates a new aperture, only accessible for logged in users

    Returns:
        based on the validation of the form, either redirects to this resources index
        page or renders the Create page again with validation errors (WTForms) or integrity errors (SQL constraints)

    """

    # convert request.form to form object
    form = AperturesForm(request.form)
    # if the form is not valid, redirect to the new page and pass the values from the form
    if not form.validate():
        return render_template('resources/apertures/new.html', form=form)
    # if the form is valid, create a new lens and redirect to the index page
    else:
        # if unique constraint is violated, inform the user
        try:
            aperture = Aperture(size=form.size.data)
            db.session.add(aperture)
            db.session.commit()
            return redirect(url_for('apertures.index'))
        except sqlalchemy.exc.IntegrityError:
            flash('Diese Größe existiert bereits', 'danger')
            return render_template('resources/apertures/new.html', form=form)


@bp.route('/<aperture_id>/edit', methods=['GET'])
@login_required
def edit(aperture_id):
    """
        Edit page for apertures, only accessible for logged in users

    Args:
        aperture_id (int):  id of the aperture to edit, passed as a parameter in the url

    Returns:
        rendered template of the edit page, with the form for editing an aperture
    """
    aperture = db.session.query(Aperture).filter(Aperture.id == aperture_id).first()
    form = AperturesForm(obj=aperture)
    return render_template('resources/apertures/edit.html', form=form)


@bp.route('/<aperture_id>/edit', methods=['POST'])
@login_required
def edit_post(aperture_id):
    """
        Edits the aperture, only accessible for logged in users

    Args:
        aperture_id (int): id of the aperture to edit, passed as a parameter in the url

    Returns:
        based on the validation of the form, either redirects to this resources index
        page or renders the Create page again with validation errors (WTForms) or integrity errors (SQL constraints)
     """
    # convert request.form to form object
    form = AperturesForm(request.form)
    # if the form is not valid, redirect to the new page and pass the values from the form
    if not form.validate():
        return render_template('resources/apertures/edit.html', form=form)
    # if the form is valid, create a new aperture and redirect to the index page
    else:
        # if unique constraint is violated, inform the user
        try:
            aperture = db.session.query(Aperture).filter(Aperture.id == aperture_id).first()
            aperture.size = form.size.data
            db.session.add(aperture)
            db.session.commit()
            return redirect(url_for('apertures.index'))
        except sqlalchemy.exc.IntegrityError:
            flash('Diese Größe existiert bereits', 'danger')
            return render_template('resources/apertures/edit.html', form=form)


@bp.route('/<aperture_id>/delete', methods=['GET', 'POST'])
@login_required
def delete(aperture_id):
    """
        Deletes the aperture only if not used in a compound, only accessible for logged in users

    Args:
        aperture_id (int): id of the aperture to delete, passed as a parameter in the url

    Returns:
        redirects to the index page, with a flash message whether the deletion was successful or not (+ possible problem)
    """
    try:
        aperture = db.session.query(Aperture).filter(Aperture.id == aperture_id).first()
        db.session.delete(aperture)
        db.session.commit()
        flash("Apertur wurde gelöscht", 'success')
        return redirect(url_for('apertures.index'))
    except sqlalchemy.exc.IntegrityError:
        flash('Diese Apertur wird noch verwendet und kann daher nicht gelöscht werden.', 'danger')
        return redirect(url_for('apertures.index'))
    except:
        flash('Apertur konnte nicht gelöscht werden. Probieren Sie es später erneut.', 'danger')
        return redirect(url_for('apertures.index'))
