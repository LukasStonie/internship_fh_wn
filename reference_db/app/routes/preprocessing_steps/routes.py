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
    """
        Index page for preprocessing_steps, only accessible for logged in users. Allowing the user to add, edit and delete prprocessing_steps
        
    Returns:
        rendered template of the index page, with all the preprocessing_steps
        allowing the user to add, edit and delete preprocessing_steps
    """
    preprocessing_steps = db.session.query(PreprocessingSteps).all()
    return render_template('resources/preprocessing_steps/index.html', preprocessing_steps=preprocessing_steps)


@bp.route('/new', methods=['GET'])
@login_required
def new():
    """
        Create page for preprocessing_steps, only accessible for logged in users
        
    Returns:
        rendered template of the new page, with the form for creating a new preprocessing_step
    """
    form = PreprocessingStepsForm()
    return render_template('resources/preprocessing_steps/new.html', form=form)


@bp.route('/new', methods=['POST'])
@login_required
def new_post():
    """
        Creates a new preprocessing_step, only accessible for logged in users
        
    Returns:
        based on the validation of the form, either redirects to this resources index page or 
        renders the Create page again with validation errors (WTForms) or integrity errors (SQL constraints)
    """
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
    """
        Edit page for preprocessing_steps, only accessible for logged in users
        
    Args:
        preprocessing_step_id (int): id of the preprocessing_step to be edited

    Returns:
        rendered template of the edit page, with the form for editing a preprocessing_step
    """
    preprocessing_step = db.session.query(PreprocessingSteps).filter(
        PreprocessingSteps.id == preprocessing_step_id).first()
    form = PreprocessingStepsForm(obj=preprocessing_step)
    return render_template('resources/preprocessing_steps/edit.html', form=form)


@bp.route('/<preprocessing_step_id>/edit', methods=['POST'])
@login_required
def edit_post(preprocessing_step_id):
    """
        Edits the preprocessing_step, only accessible for logged in users
        
    Args:
        preprocessing_step_id (int): id of the preprocessing_step to be edited

    Returns:
        based on the validation of the form, either redirects to this resources index page or 
        renders the Edit page again with validation errors (WTForms) or integrity errors (SQL constraints)
    """
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
    """
        Deletes the preprocessing_step if not used in spectrum, only accessible for logged in users
        
    Args:
        preprocessing_step_id (int): id of the preprocessing_step to be deleted

    Returns:
        redirects to the index page with a flash message based on the success of the deletion
    """
    try:
        preprocessing_step = db.session.query(PreprocessingSteps).filter(
            PreprocessingSteps.id == preprocessing_step_id).first()
        # db.session.delete(preprocessing_step) # does not honor the foreign key constraint
        # deleting with the delete function does not work
        # because of the foreign key constraint
        # therefore, we use the execute function
        db.session.execute(f"DELETE FROM preprocessing_steps where id = :id", {"id": preprocessing_step.id})
        db.session.commit()
        flash("Vorverarbeitungsschritt wurde gelöscht", 'success')
        return redirect(url_for('preprocessing_steps.index'))
    except sqlalchemy.exc.IntegrityError:
        flash("Dieser Vorverarbeitungsschritt wird noch verwendet und kann daher nicht gelöscht werden", 'danger')
        return redirect(url_for('preprocessing_steps.index'))
    except:
        flash("Vorverarbeitungsschritt konnte nicht gelöscht werden", 'danger')
        return redirect(url_for('preprocessing_steps.index'))
