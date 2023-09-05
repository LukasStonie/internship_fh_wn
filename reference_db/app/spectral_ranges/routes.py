import sqlalchemy.exc
from flask import render_template, request, url_for, flash, redirect
from app.spectral_ranges import bp
from app.models.model import SpectralRange
from app.extensions import db


def validate_form(form):
    # check if the form is valid
    form_ok = True
    # check every field if it is empty
    # set form_ok to False if any field is empty
    if not form['start']:
        flash('Start ist ein Pflichtfeld', 'error')
        form_ok = False
    if not form['end']:
        flash('Ende ist ein Pflichtfeld', 'error')
        form_ok = False
    # return whether form is valid
    # return the values from the form for new slide or redirect
    return form_ok, form['start'], form['end']


@bp.route('/')
def index():
    spectral_ranges = db.session.query(SpectralRange).all()
    return render_template('spectral_ranges/index.html', spectral_ranges=spectral_ranges)


@bp.route('/new', methods=['GET', 'POST'])
def new():
    # if the request method is POST, the form was submitted
    # validate the form and create a new slide
    if request.method == 'POST':
        # validate form
        # form_ok signifies if the form is valid or not
        # name is the value from the form
        form_ok, start, end = validate_form(request.form)
        # if the form is not valid, redirect to the new page and pass the values from the form
        if not form_ok:
            return redirect(url_for('spectral_ranges.new', start=start, end=end))
        # if the form is valid, create a new slide and redirect to the index page
        else:
            # if unique constraint is violated, inform the user
            try:
                spectral_range = SpectralRange(start=start, end=end)
                db.session.add(spectral_range)
                db.session.commit()
                return redirect(url_for('spectral_ranges.index'))
            except sqlalchemy.exc.IntegrityError:
                flash('Diese Kombination aus Start und Ende existiert bereits', 'error')
                return redirect(url_for('spectral_ranges.new', start=start, end=end))
    # if the request method is GET, the user wants to display the form
    else:
        return render_template('spectral_ranges/new.html', values=request.args)


@bp.route('/<spectral_range_id>/edit', methods=['GET', 'POST'])
def edit(spectral_range_id):
    # if the request method is POST, the form was submitted
    # validate the form and create a new slide
    if request.method == 'POST':
        # validate form
        # form_ok signifies if the form is valid or not
        # name is the value from the form
        form_ok, start, end = validate_form(request.form)
        # if the form is not valid, redirect to the new page and pass the values from the form
        if not form_ok:
            return redirect(url_for('spectral_ranges.edit', spectral_range_id=spectral_range_id, start=start, end=end))
        # if the form is valid, create a new slide and redirect to the index page
        else:
            # if unique constraint is violated, inform the user
            try:
                spectral_range = db.session.query(SpectralRange).filter(SpectralRange.id == spectral_range_id).first()
                spectral_range.start = start
                spectral_range.end = end
                db.session.commit()
                return redirect(url_for('spectral_ranges.index'))
            except sqlalchemy.exc.IntegrityError:
                flash('Diese Kombination aus Start und Ende existiert bereits', 'error')
                return redirect(url_for('spectral_ranges.edit', spectral_range_id=spectral_range_id, start=start, end=end))
    else:
        # if the request method is GET, the user wants to display the form
        # if request.args is empty, there was no attempt to submit the form
        # if request.args is not empty, the form was submitted but validation failed and the values from the form are passed
        args_len = len(request.args.keys())
        spectral_range = vars(db.session.query(SpectralRange).filter(SpectralRange.id == spectral_range_id).first()) \
            if args_len == 0 \
            else request.args
        return render_template('spectral_ranges/edit.html', spectral_range=spectral_range)


@bp.route('/<spectral_range_id>/delete')
def delete(spectral_range_id):
    spectral_range = db.session.query(SpectralRange).filter(SpectralRange.id == spectral_range_id).first()
    db.session.delete(spectral_range)
    db.session.commit()
    return redirect(url_for('spectral_ranges.index'))
