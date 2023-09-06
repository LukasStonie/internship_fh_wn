import sqlalchemy.exc
from flask import render_template, request, url_for, flash, redirect
from app.routes.preprocessing_steps import bp
from app.models.model import PreprocessingSteps
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
    preprocessing_steps = db.session.query(PreprocessingSteps).all()
    return render_template('resources/preprocessing_steps/index.html', preprocessing_steps=preprocessing_steps)


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
            return redirect(url_for('preprocessing_steps.new', name=name))
        # if the form is valid, create a new slide and redirect to the index page
        else:
            # if unique constraint is violated, inform the user
            try:
                preprocessing_step = PreprocessingSteps(name=name)
                db.session.add(preprocessing_step)
                db.session.commit()
                return redirect(url_for('preprocessing_steps.index'))
            except sqlalchemy.exc.IntegrityError:
                flash('Diese Bezeichnung existiert bereits', 'error')
                return redirect(url_for('preprocessing_steps.new', name=name))
    # if the request method is GET, the user wants to display the form
    else:
        return render_template('resources/preprocessing_steps/new.html', values=request.args)


@bp.route('/<preprocessing_step_id>/edit', methods=['GET', 'POST'])
def edit(preprocessing_step_id):
    # if the request method is POST, the form was submitted
    # validate the form and create a new slide
    if request.method == 'POST':
        # validate form
        # form_ok signifies if the form is valid or not
        # name is the value from the form
        form_ok, name = validate_form(request.form)
        # if the form is not valid, redirect to the new page and pass the values from the form
        if not form_ok:
            return redirect(url_for('preprocessing_steps.edit', name=name))
        # if the form is valid, create a new slide and redirect to the index page
        else:
            # if unique constraint is violated, inform the user
            try:
                preprocessing_step = db.session.query(PreprocessingSteps).filter_by(id=preprocessing_step_id).first()
                preprocessing_step.name = name
                db.session.commit()
                return redirect(url_for('preprocessing_steps.index'))
            except sqlalchemy.exc.IntegrityError:
                flash('Diese Bezeichnung existiert bereits', 'error')
                return redirect(url_for('preprocessing_steps.edit', name=name))
    else:
        # if the request method is GET, the user wants to display the form
        # if request.args is empty, there was no attempt to submit the form
        # if request.args is not empty, the form was submitted but validation failed and the values from the form are passed
        args_len = len(request.args.keys())
        preprocessing_step = vars(db.session.query(PreprocessingSteps).filter(PreprocessingSteps.id == preprocessing_step_id).first()) \
            if args_len == 0 \
            else request.args
        return render_template('resources/preprocessing_steps/edit.html', preprocessing_step=preprocessing_step)


@bp.route('/<preprocessing_step_id>/delete', methods=['GET', 'POST'])
def delete(preprocessing_step_id):
    preprocessing_step = db.session.query(PreprocessingSteps).filter(PreprocessingSteps.id == preprocessing_step_id).first()
    db.session.delete(preprocessing_step)
    db.session.commit()
    return redirect(url_for('preprocessing_steps.index'))