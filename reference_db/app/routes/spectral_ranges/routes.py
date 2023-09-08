import sqlalchemy.exc
from flask import render_template, request, url_for, flash, redirect
from flask_login import login_required

from app.forms.forms import SpectralRangesForm
from app.routes.spectral_ranges import bp
from app.models.model import SpectralRange
from app.extensions import db


@bp.route('/')
@login_required
def index():
    spectral_ranges = db.session.query(SpectralRange).all()
    return render_template('resources/spectral_ranges/index.html', spectral_ranges=spectral_ranges)


@bp.route('/new', methods=['GET'])
@login_required
def new():
    form = SpectralRangesForm()
    return render_template('resources/spectral_ranges/new.html', form=form)


@bp.route('/new', methods=['POST'])
@login_required
def new_post():
    # convert request.form to form object
    form = SpectralRangesForm(request.form)
    # if the form is not valid, redirect to the new page and pass the values from the form
    if not form.validate():
        return render_template('resources/spectral_ranges/new.html', form=form)
    # if the form is valid, create a new slide and redirect to the index page
    else:
        # if unique constraint is violated, inform the user
        try:
            spectral_range = SpectralRange(start=form.start.data, end=form.end.data)
            db.session.add(spectral_range)
            db.session.commit()
            return redirect(url_for('spectral_ranges.index'))
        except sqlalchemy.exc.IntegrityError:
            flash('Diese Kombination aus Start und Ende existiert bereits', 'error')
            return render_template('resources/spectral_ranges/new.html', form=form)


@bp.route('/<spectral_range_id>/edit', methods=['GET'])
@login_required
def edit(spectral_range_id):
    spectral_range = db.session.query(SpectralRange).filter(SpectralRange.id == spectral_range_id).first()
    form = SpectralRangesForm(obj=spectral_range)
    return render_template('resources/spectral_ranges/edit.html', form=form)


@bp.route('/<spectral_range_id>/edit', methods=['POST'])
@login_required
def edit_post(spectral_range_id):
    # convert request.form to form object
    form = SpectralRangesForm(request.form)
    # if the form is not valid, redirect to the new page and pass the values from the form
    if not form.validate():
        return render_template('resources/spectral_ranges/edit.html', form=form)
    # if the form is valid, create a new slide and redirect to the index page
    else:
        # if unique constraint is violated, inform the user
        try:
            spectral_range = db.session.query(SpectralRange).filter(SpectralRange.id == spectral_range_id).first()
            spectral_range.start = form.start.data
            spectral_range.end = form.end.data
            db.session.commit()
            return redirect(url_for('spectral_ranges.index'))
        except sqlalchemy.exc.IntegrityError:
            flash('Diese Kombination aus Start und Ende existiert bereits', 'error')
            return render_template('resources/spectral_ranges/edit.html', form=form)


@bp.route('/<spectral_range_id>/delete')
@login_required
def delete(spectral_range_id):
    spectral_range = db.session.query(SpectralRange).filter(SpectralRange.id == spectral_range_id).first()
    db.session.delete(spectral_range)
    db.session.commit()
    return redirect(url_for('spectral_ranges.index'))
