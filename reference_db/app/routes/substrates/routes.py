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
    substrates = db.session.query(Substrate).all()
    return render_template('resources/substrates/index.html', substrates=substrates)


@bp.route('/new', methods=['GET'])
@login_required
def new():
    form = SubstratesForm()
    return render_template('resources/substrates/new.html', form=form)


@bp.route('/new', methods=['POST'])
@login_required
def new_post():
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
    substrate = db.session.query(Substrate).filter(Substrate.id == substrate_id).first()
    form = SubstratesForm(obj=substrate)
    return render_template('resources/substrates/edit.html', form=form, substrate=substrate)


@bp.route('/<substrate_id>/edit', methods=['POST'])
@login_required
def edit_post(substrate_id):
    # convert request.form to form object
    form = SubstratesForm(request.form)
    # if the form is not valid, redirect to the new page and pass the values from the form
    if not form.validate():
        return render_template('resources/substrates/edit.html', form=form)
    # if the form is valid, create a new slide and redirect to the index page
    else:
        # if unique constraint is violated, inform the user
        try:
            has_file = len(request.files) != 0 and request.files['instructions'] is not None
            substrate = db.session.query(Substrate).filter(Substrate.id == substrate_id).first()

            substrate.name = form.name.data
            if has_file:
                substrate.filename = request.files['instructions'].filename
                substrate.instruction = request.files['instructions'].read()
            db.session.commit()
            return redirect(url_for('substrates.index'))
        except sqlalchemy.exc.IntegrityError:
            flash('Diese Bezeichnung existiert bereits', 'danger')
            return render_template('resources/substrates/edit.html', form=form)


@bp.route('/<substrate_id>/delete', methods=['GET', 'POST'])
@login_required
def delete(substrate_id):
    substrate = db.session.query(Substrate).filter(Substrate.id == substrate_id).first()
    db.session.delete(substrate)
    db.session.commit()
    return redirect(url_for('substrates.index'))


@bp.route('/<substrate_id>/download', methods=['GET', 'POST'])
def download(substrate_id):
    print(substrate_id)
    substrate = db.session.query(Substrate).filter(Substrate.id == substrate_id).first()
    return send_file(BytesIO(substrate.instruction), download_name=f'{substrate.filename}', as_attachment=True)


@bp.route('/<substrate_id>/removefile', methods=['GET', 'POST'])
def remove_file(substrate_id):
    substrate = db.session.query(Substrate).filter(Substrate.id == substrate_id).first()
    substrate.instruction = None
    substrate.filename = None
    db.session.commit()
    return redirect(url_for('substrates.edit', substrate_id=substrate_id))
