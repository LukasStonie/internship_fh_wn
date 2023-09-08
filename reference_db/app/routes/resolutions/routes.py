import sqlalchemy.exc
from flask import render_template, request, url_for, flash, redirect
from flask_login import login_required

from app.forms.forms import ResolutionsForm
from app.routes.resolutions import bp
from app.models.model import Resolution
from app.extensions import db


@bp.route('/')
@login_required
def index():
    resolutions = db.session.query(Resolution).all()
    return render_template('resources/resolutions/index.html', resolutions=resolutions)


@bp.route('/new', methods=['GET'])
@login_required
def new():
    form = ResolutionsForm()
    return render_template('resources/resolutions/new.html', form=form)


@bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_post():
    # convert request.form to a form object
    form = ResolutionsForm(request.form)
    # if the form is not valid, redirect to the new page and pass the values from the form
    if not form.validate():
        return render_template('resources/resolutions/new.html', form=form)
    # if the form is valid, create a new slide and redirect to the index page
    else:
        # if unique constraint is violated, inform the user
        try:
            resolution = Resolution(description=form.description.data)
            db.session.add(resolution)
            db.session.commit()
            return redirect(url_for('resolutions.index'))
        except sqlalchemy.exc.IntegrityError:
            flash('Diese Bezeichnung existiert bereits', 'error')
            return render_template('resources/resolutions/new.html', form=form)


@bp.route('/<resolution_id>/edit', methods=['GET'])
@login_required
def edit(resolution_id):
    resolution = db.session.query(Resolution).filter_by(id=resolution_id).first()
    form = ResolutionsForm(obj=resolution)
    return render_template('resources/resolutions/edit.html', form=form)


@bp.route('/<resolution_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(resolution_id):
    # convert request.form to a form object
    form = ResolutionsForm(request.form)
    # if the form is not valid, redirect to the new page and pass the values from the form
    if not form.validate():
        return render_template('resources/resolutions/edit.html', form=form)
    # if the form is valid, create a new slide and redirect to the index page
    else:
        # if unique constraint is violated, inform the user
        try:
            resolution = db.session.query(Resolution).filter_by(id=resolution_id).first()
            resolution.description = form.description.data
            db.session.commit()
            return redirect(url_for('resolutions.index'))
        except sqlalchemy.exc.IntegrityError:
            flash('Diese Bezeichnung existiert bereits', 'error')
            return render_template('resources/resolutions/edit.html', form=form)


@bp.route('/<resolution_id>/delete', methods=['GET', 'POST'])
@login_required
def delete(resolution_id):
    resolution = db.session.query(Resolution).filter_by(id=resolution_id).first()
    db.session.delete(resolution)
    db.session.commit()
    return redirect(url_for('resolutions.index'))
