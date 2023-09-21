from io import BytesIO
import sqlalchemy.exc
from flask import render_template, request, url_for, flash, redirect, send_file
from flask_login import login_required

from app.forms.forms import SubstratesForm
from app.routes.substrates import bp
from app.models.model import Substrate
from app.extensions import db


@bp.route('/')
@login_required
def index():
    """
        Index page for substrates, only accessible for logged in users. Allowing the the user to add, edit and delete substrates

    Returns:
        rendered template of the index page, with all the substrates
    """
    substrates = db.session.query(Substrate).all()
    return render_template('resources/substrates/index.html', substrates=substrates)


@bp.route('/new', methods=['GET'])
@login_required
def new():
    """
        Create page for substrates, only accessible for logged in users

    Returns:
        rendered template of the new page, with the form for creating a new substrate
    """
    form = SubstratesForm()
    return render_template('resources/substrates/new.html', form=form)


@bp.route('/new', methods=['POST'])
@login_required
def new_post():
    """
        Creates a new substrate if form is valid, only accessible for logged in users

    Returns:
        based on the validation of the form, either redirects to this resources index page or
        renders the Create page again with validation errors (WTForms) or integrity errors (SQL constraints)
    """
    # convert request.form to form object
    form = SubstratesForm(request.form)
    # if the form is not valid, redirect to the new page and pass the values from the form
    if not form.validate():
        return render_template('resources/substrates/new.html', form=form)
    # if the form is valid, create a new slide and redirect to the index page
    else:
        # if unique constraint is violated, inform the user
        try:
            has_file = request.files['instructions'] is not None
            substrate = None
            if not has_file:
                substrate = Substrate(name=form.name.data)
            else:
                file = form.instructions.data
                substrate = Substrate(name=form.name.data, filename=request.files['instructions'].filename,
                                      instruction=request.files['instructions'].read())
            db.session.add(substrate)
            db.session.commit()
            return redirect(url_for('substrates.index'))
        except sqlalchemy.exc.IntegrityError:
            flash('Diese Bezeichnung existiert bereits', 'danger')
            return render_template('resources/substrates/new.html', form=form)


@bp.route('/<substrate_id>/edit', methods=['GET'])
@login_required
def edit(substrate_id):
    """
        Edit page for substrates, only accessible for logged in users

    Args:
        substrate_id (int): id of the substrate to be edited

    Returns:
        rendered template of the edit page, with the form for editing the substrate
    """
    substrate = db.session.query(Substrate).filter(Substrate.id == substrate_id).first()
    form = SubstratesForm(obj=substrate)
    return render_template('resources/substrates/edit.html', form=form, substrate=substrate)


@bp.route('/<substrate_id>/edit', methods=['POST'])
@login_required
def edit_post(substrate_id):
    """
        Edits the substrate if form is valid, only accessible for logged in users

    Args:
        substrate_id (int): id of the substrate to be edited

    Returns:
        based on the validation of the form, either redirects to this resources index page or
        renders the Create page again with validation errors (WTForms) or integrity errors (SQL constraints)
    """
    # convert request.form to form object
    form = SubstratesForm(request.form)
    # if the form is not valid, redirect to the new page and pass the values from the form
    if not form.validate():
        return render_template('resources/substrates/edit.html', form=form)
    # if the form is valid, create a new slide and redirect to the index page
    else:
        # if unique constraint is violated, inform the user
        substrate = db.session.query(Substrate).filter(Substrate.id == substrate_id).first()
        try:
            # check if a file was uploaded (replace the old one
            has_file = len(request.files) != 0 and request.files['instructions'] is not None

            # update name
            substrate.name = form.name.data

            # update file if necessary
            if has_file:
                substrate.filename = request.files['instructions'].filename
                substrate.instruction = request.files['instructions'].read()
            db.session.commit()
            return redirect(url_for('substrates.index'))
        except sqlalchemy.exc.IntegrityError:
            flash('Diese Bezeichnung existiert bereits', 'danger')
            db.session.rollback()
            return render_template('resources/substrates/edit.html', form=form, substrate=substrate)


@bp.route('/<substrate_id>/delete', methods=['GET', 'POST'])
@login_required
def delete(substrate_id):
    """
        Deletes the substrate, only accessible for logged in users

    Args:
        substrate_id (int): id of the substrate to be deleted

    Returns:
        redirects to the index page, with a flash message based on the success of the deletion
    """
    try:
        substrate = db.session.query(Substrate).filter(Substrate.id == substrate_id).first()
        # db.session.delete(substrate) # not honoring the foreign key constraint
        # deleting with the delete function does not work
        # because of the foreign key constraint
        # therefore, we use the execute function
        db.session.execute(f"DELETE FROM substrates WHERE id = :id", {"id": substrate_id})
        db.session.commit()
        flash("Substrat wurde gelöscht", 'success')
        return redirect(url_for('substrates.index'))
    except sqlalchemy.exc.IntegrityError:
        flash("Dieses Substrat wird noch verwendet und kann daher nicht gelöscht werden", 'danger')
        return redirect(url_for('substrates.index'))
    except:
        flash("Substrat kann nicht gelöscht werden", 'danger')
        return redirect(url_for('substrates.index'))


@bp.route('/<substrate_id>/download', methods=['GET', 'POST'])
def download(substrate_id):
    """
        Allows user to download the instruction file of a substrate

    Args:
        substrate_id (int): id of the substrate instruction to be downloaded

    Returns:
        the instruction as a downloadable file
    """
    substrate = db.session.query(Substrate).filter(Substrate.id == substrate_id).first()
    return send_file(BytesIO(substrate.instruction), download_name=f'{substrate.filename}', as_attachment=True)


@bp.route('/<substrate_id>/removefile', methods=['GET', 'POST'])
def remove_file(substrate_id):
    """
        Removes the instruction file of a substrate

    Args:
        substrate_id (int): id of the substrate instruction to be removed

    Returns:
        redirects to the edit page of the substrate
    """
    substrate = db.session.query(Substrate).filter(Substrate.id == substrate_id).first()
    substrate.instruction = None
    substrate.filename = None
    db.session.commit()
    return redirect(url_for('substrates.edit', substrate_id=substrate_id))
