import sqlalchemy.exc
from flask import render_template, request, url_for, flash, redirect
from flask_login import login_required

from app.forms.forms import PreprocessingStepsForm
from app.routes.preprocessing_steps import bp
from app.models.model import PreprocessingSteps
from app.extensions import db


@bp.route('/')
@login_required
def index():
    preprocessing_steps = db.session.query(PreprocessingSteps).all()
    return render_template('resources/preprocessing_steps/index.html', preprocessing_steps=preprocessing_steps)


@bp.route('/new', methods=['GET'])
@login_required
def new():
    form = PreprocessingStepsForm()
    return render_template('resources/preprocessing_steps/new.html', form=form)


@bp.route('/new', methods=['POST'])
@login_required
def new_post():
    # convert request.form to form object
    form = PreprocessingStepsForm(request.form)
    # if the form is not valid, redirect to the new page and pass the values from the form
    if not form.validate():
        return render_template('resources/preprocessing_steps/new.html', form=form)
    # if the form is valid, create a new slide and redirect to the index page
    else:
        # if unique constraint is violated, inform the user
        try:
            preprocessing_step = PreprocessingSteps(name=form.name.data)
            db.session.add(preprocessing_step)
            db.session.commit()
            return redirect(url_for('preprocessing_steps.index'))
        except sqlalchemy.exc.IntegrityError:
            flash('Diese Bezeichnung existiert bereits', 'danger')
            return render_template('resources/preprocessing_steps/new.html', form=form)


@bp.route('/<preprocessing_step_id>/edit', methods=['GET'])
@login_required
def edit(preprocessing_step_id):
    preprocessing_step = db.session.query(PreprocessingSteps).filter(
        PreprocessingSteps.id == preprocessing_step_id).first()
    form = PreprocessingStepsForm(obj=preprocessing_step)
    return render_template('resources/preprocessing_steps/edit.html', form=form)


@bp.route('/<preprocessing_step_id>/edit', methods=['POST'])
@login_required
def edit_post(preprocessing_step_id):
    # convert request.form to form object
    form = PreprocessingStepsForm(request.form)
    # if the form is not valid, redirect to the new page and pass the values from the form
    if not form.validate():
        return render_template('resources/preprocessing_steps/edit.html', form=form)
    # if the form is valid, create a new slide and redirect to the index page
    else:
        # if unique constraint is violated, inform the user
        try:
            preprocessing_step = db.session.query(PreprocessingSteps).filter_by(id=preprocessing_step_id).first()
            preprocessing_step.name = form.name.data
            db.session.commit()
            return redirect(url_for('preprocessing_steps.index'))
        except sqlalchemy.exc.IntegrityError:
            flash('Diese Bezeichnung existiert bereits', 'danger')
            return render_template('resources/preprocessing_steps/edit.html', form=form)


@bp.route('/<preprocessing_step_id>/delete', methods=['GET', 'POST'])
@login_required
def delete(preprocessing_step_id):
    preprocessing_step = db.session.query(PreprocessingSteps).filter(
        PreprocessingSteps.id == preprocessing_step_id).first()
    db.session.delete(preprocessing_step)
    db.session.commit()
    return redirect(url_for('preprocessing_steps.index'))
