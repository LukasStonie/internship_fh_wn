import sqlalchemy.exc
from flask import render_template, request, url_for, flash, redirect
from flask_login import login_required

from app.forms.forms import IntensityForm
from app.routes.intensities import bp

from app.models.model import Intensity

from app.extensions import db

@bp.route('/')
@login_required
def index():
    intensities = db.session.query(Intensity).all()
    return render_template('resources/intensities/index.html', intensities=intensities)


@bp.route('/new', methods=['GET'])
@login_required
def new():
    form = IntensityForm()
    return render_template('resources/intensities/new.html', form=form)


@bp.route('/new', methods=['POST'])
@login_required
def new_post():
    # convert request.form to form object
    form = IntensityForm(request.form)
    # if the form is not valid, redirect to the new page and pass the values from the form
    if not form.validate():
        return render_template('resources/intensities/new.html', form=form)
    # if the form is valid, create a new slide and redirect to the index page
    else:
        # if unique constraint is violated, inform the user
        try:
            intensity = Intensity(shorthand=form.shorthand.data, description=form.description.data)
            db.session.add(intensity)
            db.session.commit()
            return redirect(url_for('intensities.index'))
        except sqlalchemy.exc.IntegrityError:
            flash('Diese Bezeichnung existiert bereits', 'danger')
            return render_template('resources/intensities/new.html', form=form)


@bp.route('/<intensity_id>/edit', methods=['GET'])
@login_required
def edit(intensity_id):
    intensity = db.session.query(Intensity).filter(Intensity.id == intensity_id).first()
    form = IntensityForm(obj=intensity)
    return render_template('resources/intensities/edit.html', form=form)


@bp.route('/<intensity_id>/edit', methods=['POST'])
@login_required
def edit_post(intensity_id):
    # convert request.form to form object
    form = IntensityForm(request.form)
    # if the form is not valid, redirect to the new page and pass the values from the form
    if not form.validate():
        return render_template('resources/intensities/edit.html', form=form)
    # if the form is valid, create a new slide and redirect to the index page
    else:
        # if unique constraint is violated, inform the user
        try:
            intensity = db.session.query(Intensity).filter(Intensity.id == intensity_id).first()
            intensity.shorthand = form.shorthand.data
            intensity.description = form.description.data
            db.session.add(intensity)
            db.session.commit()
            return redirect(url_for('intensities.index'))
        except sqlalchemy.exc.IntegrityError:
            flash('Diese Bezeichnung existiert bereits', 'danger')
            return render_template('resources/intensities/edit.html', form=form)


@bp.route('/<intensity_id>/delete', methods=['GET'])
@login_required
def delete(intensity_id):
    try:
        intensity = db.session.query(Intensity).filter(Intensity.id == intensity_id).first()
        db.session.delete(intensity)
        db.session.commit()
        return redirect(url_for('intensities.index'))
    except sqlalchemy.exc.IntegrityError:
        flash('Diese Intensität wird noch verwendet und kann daher nicht gelöscht werden', 'danger')
        return redirect(url_for('intensities.index'))
    except:
        flash('Intensität konnte nicht gelöscht werden. Probieren Sie es später erneut', 'danger')
        return redirect(url_for('intensities.index'))