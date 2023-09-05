from io import BytesIO
import sqlalchemy.exc
from flask import render_template, request, url_for, flash, redirect, send_file
from app.substrates import bp
from app.models.model import Substrate
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
    substrates = db.session.query(Substrate).all()
    return render_template('substrates/index.html', substrates=substrates)


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
            return redirect(url_for('substrates.new', name=name))
        # if the form is valid, create a new slide and redirect to the index page
        else:
            # if unique constraint is violated, inform the user
            try:
                has_file = request.files['instruction'] is not None

                substrate = Substrate(name=name)if not has_file \
                            else Substrate(name=name, instruction=request.files['instruction'].read())
                db.session.add(substrate)
                db.session.commit()
                return redirect(url_for('substrates.index'))
            except sqlalchemy.exc.IntegrityError:
                flash('Diese Bezeichnung existiert bereits', 'error')
                return redirect(url_for('substrates.new', name=name))
    # if the request method is GET, the user wants to display the form
    else:
        return render_template('substrates/new.html', values=request.args)


@bp.route('/<substrate_id>/edit', methods=['GET', 'POST'])
def edit(substrate_id):
    # if the request method is POST, the form was submitted
    # validate the form and create a new slide
    if request.method == 'POST':
        # validate form
        # form_ok signifies if the form is valid or not
        # name is the value from the form
        form_ok, name = validate_form(request.form)
        # if the form is not valid, redirect to the new page and pass the values from the form
        if not form_ok:
            return redirect(url_for('substrates.edit', name=name))
        # if the form is valid, create a new slide and redirect to the index page
        else:
            # if unique constraint is violated, inform the user
            try:
                has_file = request.files['instruction_new'] is not None
                is_empty = request.files['instruction_new'].content_length == 0
                substrate = db.session.query(Substrate).filter(Substrate.id == substrate_id).first()
                substrate.name = name
                if has_file and not is_empty:
                    substrate.instruction = request.files['instruction_new'].read()
                db.session.commit()
                return redirect(url_for('substrates.index'))
            except sqlalchemy.exc.IntegrityError:
                flash('Diese Bezeichnung existiert bereits', 'error')
                return redirect(url_for('substrates.edit', name=name))
    # if the request method is GET, the user wants to display the form
    else:
        substrate = db.session.query(Substrate).filter(Substrate.id == substrate_id).first()
        return render_template('substrates/edit.html', substrate=substrate)


@bp.route('/<substrate_id>/delete', methods=['GET', 'POST'])
def delete(substrate_id):
    substrate = db.session.query(Substrate).filter(Substrate.id == substrate_id).first()
    db.session.delete(substrate)
    db.session.commit()
    return redirect(url_for('substrates.index'))


@bp.route('/<substrate_id>/download', methods=['GET', 'POST'])
def download(substrate_id):
    print(substrate_id)
    substrate = db.session.query(Substrate).filter(Substrate.id == substrate_id).first()
    return send_file(BytesIO(substrate.instruction), download_name=f'{substrate.name}_instruction.pdf', as_attachment=True)