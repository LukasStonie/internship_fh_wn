import sqlalchemy.exc
from flask import render_template, request, url_for, flash, redirect
from app.routes.resolutions import bp
from app.models.model import Resolution
from app.extensions import db


def validate_form(form):
    # check if the form is valid
    form_ok = True
    # check every field if it is empty
    # set form_ok to False if any field is empty
    if not form['description']:
        flash('Bezeichnung ist ein Pflichtfeld', 'error')
        form_ok = False
    # return whether form is valid
    # return the values from the form for new slide or redirect
    return form_ok, form['description']


@bp.route('/')
def index():
    resolutions = db.session.query(Resolution).all()
    return render_template('resources/resolutions/index.html', resolutions=resolutions)


@bp.route('/new', methods=['GET', 'POST'])
def new():
    # if the request method is POST, the form was submitted
    # validate the form and create a new slide
    if request.method == 'POST':
        # validate form
        # form_ok signifies if the form is valid or not
        # description is the value from the form
        form_ok, description = validate_form(request.form)
        # if the form is not valid, redirect to the new page and pass the values from the form
        if not form_ok:
            return redirect(url_for('resolutions.new', description=description))
        # if the form is valid, create a new slide and redirect to the index page
        else:
            # if unique constraint is violated, inform the user
            try:
                resolution = Resolution(description=description)
                db.session.add(resolution)
                db.session.commit()
                return redirect(url_for('resolutions.index'))
            except sqlalchemy.exc.IntegrityError:
                flash('Diese Bezeichnung existiert bereits', 'error')
                return redirect(url_for('resolutions.new', description=description))
    # if the request method is GET, the user wants to display the form
    else:
        return render_template('resources/resolutions/new.html', values=request.args)


@bp.route('/<resolution_id>/edit', methods=['GET', 'POST'])
def edit(resolution_id):
    # if the request method is POST, the form was submitted
    # validate the form and create a new slide
    if request.method == 'POST':
        # validate form
        # form_ok signifies if the form is valid or not
        # resolution_description is the value from the form
        form_ok, description = validate_form(request.form)
        # if the form is not valid, redirect to the new page and pass the values from the form
        if not form_ok:
            return redirect(url_for('resolutions.edit', resolution_id=resolution_id, description=description))
        # if the form is valid, create a new slide and redirect to the index page
        else:
            # if unique constraint is violated, inform the user
            try:
                resolution = db.session.query(Resolution).filter_by(id=resolution_id).first()
                resolution.description = description
                db.session.commit()
                return redirect(url_for('resolutions.index'))
            except sqlalchemy.exc.IntegrityError:
                flash('Diese Bezeichnung existiert bereits', 'error')
                return redirect(url_for('resolutions.edit', description=description))
    # if the request method is GET, the user wants to display the form
    else:
        args_len = len(request.args.keys())
        resolution = vars(
            db.session.query(Resolution).filter(Resolution.id == resolution_id).first()) \
            if args_len == 0 \
            else request.args
        return render_template('resources/resolutions/edit.html', resolution=resolution)


@bp.route('/<resolution_id>/delete', methods=['GET', 'POST'])
def delete(resolution_id):
    resolution = db.session.query(Resolution).filter_by(id=resolution_id).first()
    db.session.delete(resolution)
    db.session.commit()
    return redirect(url_for('resolutions.index'))
