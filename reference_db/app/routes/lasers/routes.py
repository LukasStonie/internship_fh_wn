import sqlalchemy.exc
from flask import render_template, request, url_for, flash, redirect
from app.routes.lasers import bp
from app.models.model import Laser
from app.extensions import db
from flask_login import login_required, current_user


def validate_form(form):
    # check if the form is valid
    form_ok = True
    # check every field if it is empty
    # set form_ok to False if any field is empty
    if not form['wavelength']:
        flash('Wellenlänge ist ein Pflichtfeld', 'zoom')
        form_ok = False
    # return whether form is valid
    # return the values from the form for new lens or redirect
    return form_ok, form['wavelength']


@bp.route('/')
@login_required
def index():
    lasers = db.session.query(Laser).all()
    return render_template('resources/lasers/index.html', lasers=lasers, name=current_user)


@bp.route('/new', methods=['GET', 'POST'])
def new():
    # if the request method is POST, the form was submitted
    # validate the form and create a new lens
    if request.method == 'POST':
        # validate form
        # form_ok signifies if the form is valid or not
        # wavelength is the values from the form
        form_ok, wavelength = validate_form(request.form)
        # if the form is not valid, redirect to the new page and pass the values from the form
        if not form_ok:
            return redirect(url_for('laser.new', wavelength=wavelength))
        # if the form is valid, create a new lens and redirect to the index page
        else:
            # if unique constraint is violated, inform the user
            try:
                lens = Laser(wavelength=wavelength)
                db.session.add(lens)
                db.session.commit()
                return redirect(url_for('lasers.index'))
            except sqlalchemy.exc.IntegrityError:
                flash('Diese Wellenlänge existiert bereits', 'error')
                return redirect(url_for('lasers.new', wavelength=wavelength))
    # if the request method is GET, the user wants to display the form
    else:
        return render_template('resources/lasers/new.html', values=request.args)


@bp.route('/<laser_id>/edit', methods=['GET', 'POST'])
def edit(laser_id):
    # if the request method is POST, the form was submitted
    # validate the form and create a new lens
    if request.method == 'POST':
        # validate form
        # form_ok signifies if the form is valid or not
        # zoom and numerical_aperture are the values from the form
        form_ok, wavelength = validate_form(request.form)
        # if the form is not valid, redirect to the new page and pass the values from the form
        if not form_ok:
            return redirect(url_for('lasers.edit', laser_id=laser_id, wavelength=wavelength))
            # if the form is valid, create a new lens and redirect to the index page
        else:
            # if unique constraint is violated, inform the user
            try:
                laser = db.session.query(Laser).filter(Laser.id == laser_id).first()
                laser.wavelength = wavelength
                db.session.commit()
                return redirect(url_for('lasers.index'))
            except sqlalchemy.exc.IntegrityError:
                flash('Diese Wellenlänge existiert bereits', 'error')
                return redirect(url_for('lasers.edit', laser_id=laser_id, wavelength=wavelength))
    else:
        # if the request method is GET, the user wants to display the form
        # if request.args is empty, there was no attempt to submit the form
        # if request.args is not empty, the form was submitted but validation failed and the values from the form are passed
        args_len = len(request.args.keys())
        laser = vars(db.session.query(Laser).filter(Laser.id == laser_id).first()) \
            if args_len == 0 \
            else request.args
        return render_template('resources/lasers/edit.html', laser=laser)


@bp.route('/<laser_id>/delete')
def delete(laser_id):
    laser = db.session.query(Laser).filter(Laser.id == laser_id).first()
    db.session.delete(laser)
    db.session.commit()
    return redirect(url_for('lasers.index'))