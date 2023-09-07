import sqlalchemy.exc
from flask import render_template, request, url_for, flash, redirect
from app.routes.apertures import bp
from app.models.model import Aperture
from app.extensions import db


def validate_form(form):
    # check if the form is valid
    form_ok = True
    # check every field if it is empty
    # set form_ok to False if any field is empty
    if not form['size']:
        flash('Größe ist ein Pflichtfeld', 'zoom')
        form_ok = False
    # return whether form is valid
    # return the values from the form for new aperture or redirect
    return form_ok, form['size']


@bp.route('/')
def index():
    apertures = db.session.query(Aperture).all()
    return render_template('resources/apertures/index.html', apertures=apertures)


@bp.route('/new', methods=['GET', 'POST'])
def new():
    # if the request method is POST, the form was submitted
    # validate the form and create a new lens
    if request.method == 'POST':
        # validate form
        # form_ok signifies if the form is valid or not
        # size is the values from the form
        form_ok, size = validate_form(request.form)
        # if the form is not valid, redirect to the new page and pass the values from the form
        if not form_ok:
            return redirect(url_for('apertures.new', size=size))
        # if the form is valid, create a new lens and redirect to the index page
        else:
            # if unique constraint is violated, inform the user
            try:
                aperture = Aperture(size=size)
                db.session.add(aperture)
                db.session.commit()
                return redirect(url_for('apertures.index'))
            except sqlalchemy.exc.IntegrityError:
                flash('Diese Größe existiert bereits', 'error')
                return redirect(url_for('apertures.new', size=size))
    # if the request method is GET, the user wants to display the form
    else:
        return render_template('resources/apertures/new.html', values=request.args)


@bp.route('/<aperture_id>/edit', methods=['GET', 'POST'])
def edit(aperture_id):
    # if the request method is POST, the form was submitted
    # validate the form and create a new aperture
    if request.method == 'POST':
        # validate form
        # form_ok signifies if the form is valid or not
        # size is the values from the form
        form_ok, size = validate_form(request.form)
        # if the form is not valid, redirect to the new page and pass the values from the form
        if not form_ok:
            return redirect(url_for('apertures.edit', aperture_id=aperture_id , size=size))
        # if the form is valid, create a new aperture and redirect to the index page
        else:
            # if unique constraint is violated, inform the user
            try:
                aperture = db.session.query(Aperture).filter(Aperture.id == aperture_id).first()
                aperture.size = size
                db.session.add(aperture)
                db.session.commit()
                return redirect(url_for('apertures.index'))
            except sqlalchemy.exc.IntegrityError:
                flash('Diese Größe existiert bereits', 'error')
                return redirect(url_for('apertures.edit', aperture_id=aperture_id, size=size))
    # if the request method is GET, the user wants to display the form
    else:
        args_len = len(request.args.keys())
        aperture = vars(db.session.query(Aperture).filter(Aperture.id == aperture_id).first()) \
            if args_len == 0 \
            else request.args
        return render_template('resources/apertures/edit.html', aperture=aperture)


@bp.route('/<aperture_id>/delete', methods=['GET', 'POST'])
def delete(aperture_id):
    aperture = db.session.query(Aperture).filter(Aperture.id == aperture_id).first()
    db.session.delete(aperture)
    db.session.commit()
    return redirect(url_for('apertures.index'))