import sqlalchemy.exc
from flask import render_template, request, url_for, flash, redirect
from app.spectra_types import bp
from app.models.model import SpectrumType
from app.extensions import db


def validate_form(form):
    # check if the form is valid
    form_ok = True
    # check every field if it is empty
    # set form_ok to False if any field is empty
    if not form['name']:
        flash('Bezeichnung ist ein Pflichtfeld', 'error')
        form_ok = False
    # return whether form is valid
    # return the values from the form for new slide or redirect
    return form_ok, form['name']


@bp.route('/')
def index():
    spectra_types = db.session.query(SpectrumType).all()
    return render_template('spectra_types/index.html', spectra_types=spectra_types)


@bp.route('/new', methods=['GET', 'POST'])
def new():
    # if the request method is POST, the form was submitted
    # validate the form and create a new slide
    if request.method == 'POST':
        # validate form
        # form_ok signifies if the form is valid or not
        # name is the value from the form
        form_ok, name = validate_form(request.form)
        # if the form is not valid, redirect to the new page and pass the values from the form
        if not form_ok:
            return redirect(url_for('spectra_types.new', name=name))
        # if the form is valid, create a new slide and redirect to the index page
        else:
            # if unique constraint is violated, inform the user
            try:
                spectrum_type = SpectrumType(name=name)
                db.session.add(spectrum_type)
                db.session.commit()
                return redirect(url_for('spectra_types.index'))
            except sqlalchemy.exc.IntegrityError:
                flash('Diese Bezeichnung existiert bereits', 'error')
                return redirect(url_for('spectra_types.new', name=name))
    # if the request method is GET, the user wants to display the form
    else:
        return render_template('spectra_types/new.html', values=request.args)


@bp.route('/<spectrum_type_id>/edit', methods=['GET', 'POST'])
def edit(spectrum_type_id):
    # if the request method is POST, the form was submitted
    # validate the form and create a new slide
    if request.method == 'POST':
        # validate form
        # form_ok signifies if the form is valid or not
        # name is the value from the form
        form_ok, name = validate_form(request.form)
        # if the form is not valid, redirect to the new page and pass the values from the form
        if not form_ok:
            return redirect(url_for('spectra_types.edit', spectrum_type_id=spectrum_type_id, name=name))
        # if the form is valid, create a new slide and redirect to the index page
        else:
            # if unique constraint is violated, inform the user
            try:
                spectrum_type = db.session.query(SpectrumType).filter_by(id=spectrum_type_id).one()
                spectrum_type.name = name
                db.session.commit()
                return redirect(url_for('spectra_types.index'))
            except sqlalchemy.exc.IntegrityError:
                flash('Diese Bezeichnung existiert bereits', 'error')
                return redirect(url_for('spectra_types.edit', spectrum_type_id=spectrum_type_id, name=name))
    # if the request method is GET, the user wants to display the form
    else:
        args_len = len(request.args.keys())
        spectrum_type = vars(db.session.query(SpectrumType).filter(SpectrumType.id == spectrum_type_id).first()) \
            if args_len == 0 \
            else request.args
        return render_template('spectra_types/edit.html', spectrum_type=spectrum_type)


@bp.route('/<spectrum_type_id>/delete')
def delete(spectrum_type_id):
    spectrum_type = db.session.query(SpectrumType).filter(SpectrumType.id == spectrum_type_id).first()
    db.session.delete(spectrum_type)
    db.session.commit()
    return redirect(url_for('spectra_types.index'))