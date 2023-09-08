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
    apertures = db.session.query(Aperture).all()
    return render_template('resources/apertures/index.html', apertures=apertures)


@bp.route('/new', methods=['GET'])
@login_required
def new():
    form = AperturesForm()
    return render_template('resources/apertures/new.html', form=form)


@bp.route('/new', methods=['POST'])
@login_required
def new_post():
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
            flash('Diese Größe existiert bereits', 'error')
            return render_template('resources/apertures/new.html', form=form)


@bp.route('/<aperture_id>/edit', methods=['GET'])
@login_required
def edit(aperture_id):
    aperture = db.session.query(Aperture).filter(Aperture.id == aperture_id).first()
    form = AperturesForm(obj=aperture)
    return render_template('resources/apertures/edit.html', form=form)


@bp.route('/<aperture_id>/edit', methods=['POST'])
@login_required
def edit_post(aperture_id):
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
            flash('Diese Größe existiert bereits', 'error')
            return render_template('resources/apertures/edit.html', form=form)


@bp.route('/<aperture_id>/delete', methods=['GET', 'POST'])
@login_required
def delete(aperture_id):
    aperture = db.session.query(Aperture).filter(Aperture.id == aperture_id).first()
    db.session.delete(aperture)
    db.session.commit()
    return redirect(url_for('apertures.index'))
