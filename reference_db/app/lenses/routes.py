import flask
import sqlalchemy.exc
from flask import render_template, request, url_for, flash, redirect
from app.lenses import bp
from app.models.model import Lens
from app.extensions import db


@bp.route('/')
def index():
    # get all lenses from database using SQLAlchemy and pass them to the template
    lenses = db.session.query(Lens).all()
    return render_template('lenses/index.html', lenses=lenses)


@bp.route('/<lens_id>/edit', methods=['GET', 'POST'])
def edit(lens_id):
    # if the request method is POST, the form was submitted
    # validate the form and create a new lens
    if request.method == 'POST':
        # validate form
        # form_ok signifies if the form is valid or not
        # zoom and numerical_aperture are the values from the form
        form_ok, zoom, numerical_aperture = validate_form(request.form)
        # if the form is not valid, redirect to the new page and pass the values from the form
        if not form_ok:
            return redirect(url_for('lenses.edit', lens_id=lens_id, zoom=zoom, numerical_aperture=numerical_aperture))
            # if the form is valid, create a new lens and redirect to the index page
        else:
            # if unique constraint is violated, inform the user
            try:
                lens = db.session.query(Lens).filter(Lens.id == lens_id).first()
                lens.zoom = zoom
                lens.numerical_aperture = numerical_aperture
                db.session.commit()
                return redirect(url_for('lenses.index'))
            except sqlalchemy.exc.IntegrityError:
                flash('Diese Kombination aus Zoom und numerischer Apertur existiert bereits', 'error')
                return redirect(url_for('lenses.edit',lens_id=lens_id, zoom=zoom, numerical_aperture=numerical_aperture))
    else:
        # if the request method is GET, the user wants to display the form
        # if request.args is empty, there was no attempt to submit the form
        # if request.args is not empty, the form was submitted but validation failed and the values from the form are passed
        args_len = len(request.args.keys())
        lens = vars(db.session.query(Lens).filter(Lens.id == lens_id).first()) \
            if args_len == 0 \
            else request.args
        return render_template('lenses/edit.html', lens=lens)


@bp.route('/<lens_id>/delete')
def delete(lens_id):
    lens = db.session.query(Lens).filter(Lens.id == lens_id).first()
    db.session.delete(lens)
    db.session.commit()
    return redirect(url_for('lenses.index'))

@bp.route('/new', methods=['GET', 'POST'])
def new():
    # if the request method is POST, the form was submitted
    # validate the form and create a new lens
    if request.method == 'POST':
        # validate form
        # form_ok signifies if the form is valid or not
        # zoom and numerical_aperture are the values from the form
        form_ok, zoom, numerical_aperture = validate_form(request.form)
        # if the form is not valid, redirect to the new page and pass the values from the form
        if not form_ok:
            return redirect(url_for('lenses.new', zoom=zoom, numerical_aperture=numerical_aperture))
        # if the form is valid, create a new lens and redirect to the index page
        else:
            # if unique constraint is violated, inform the user
            try:
                lens = Lens(zoom=zoom, numerical_aperture=numerical_aperture)
                print("before add")
                db.session.add(lens)
                print("before commit")
                db.session.commit()
                return redirect(url_for('lenses.index'))

            except sqlalchemy.exc.IntegrityError:
                flash('Diese Kombination aus Zoom und numerischer Apertur existiert bereits', 'error')
                return redirect(url_for('lenses.new', zoom=zoom, numerical_aperture=numerical_aperture))

    # if the request method is GET, the user wants to display the form
    else:

        return render_template('lenses/new.html', values=request.args)


def validate_form(form):
    # check if the form is valid
    form_ok = True
    # check every field if it is empty
    # set form_ok to False if any field is empty
    if not form['zoom']:
        flash('Zoom ist ein Pflichtfeld', 'zoom')
        form_ok = False
    if not form['numerical_aperture']:
        flash('Numerische Apertur ist ein Pflichtfeld', 'numerical_aperture')
        form_ok = False
    # return whether form is valid
    # return the values from the form for new lens or redirect
    return form_ok, form['zoom'], form['numerical_aperture']
