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
    lasers = db.session.query(Laser).all()
    return render_template('resources/lasers/index.html', lasers=lasers, name=current_user)


@bp.route('/new', methods=['GET'])
@login_required
def new():
    form = LasersForm()
    return render_template('resources/lasers/new.html', form=form)


@bp.route('/new', methods=['POST'])
@login_required
def new_post():
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
            flash('Diese Wellenlänge existiert bereits', 'error')
            return render_template('resources/lasers/new.html', form=form)


@bp.route('/<laser_id>/edit', methods=['GET'])
@login_required
def edit(laser_id):
    laser = db.session.query(Laser).filter(Laser.id == laser_id).first()
    form = LasersForm(obj=laser)
    return render_template('resources/lasers/edit.html', form=form)


@bp.route('/<laser_id>/edit', methods=['POST'])
@login_required
def edit_post(laser_id):
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
            flash('Diese Wellenlänge existiert bereits', 'error')
            return render_template('resources/lasers/edit', form=form)


@bp.route('/<laser_id>/delete')
@login_required
def delete(laser_id):
    laser = db.session.query(Laser).filter(Laser.id == laser_id).first()
    db.session.delete(laser)
    db.session.commit()
    return redirect(url_for('lasers.index'))
