import sqlalchemy.exc
from flask import render_template, request, url_for, flash, redirect

from app.forms.forms import LensesForm
from app.routes.lenses import bp
from app.models.model import Lens
from app.extensions import db
from flask_login import login_required, current_user


@bp.route('/')
@login_required
def index():
    # get all lenses from database using SQLAlchemy and pass them to the template
    lenses = db.session.query(Lens).all()
    return render_template('resources/lenses/index.html', lenses=lenses)


@bp.route('/new', methods=['GET'])
@login_required
def new():
    form = LensesForm()
    return render_template('resources/lenses/new.html', form=form)


@bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_post():
    # get the values from the form
    form = LensesForm(request.form)
    # if the form is not valid, redirect to the new page and pass the values from the form
    if not form.validate():
        return render_template('resources/lenses/new.html', form=form)
    # if the form is valid, create a new lens and redirect to the index page
    else:
        # if unique constraint is violated, inform the user
        try:
            lens = Lens(zoom=form.zoom.data, numerical_aperture=form.numerical_aperture.data)
            db.session.add(lens)
            db.session.commit()
            return redirect(url_for('lenses.index'))

        except sqlalchemy.exc.IntegrityError:
            flash('Diese Kombination aus Zoom und numerischer Apertur existiert bereits', 'danger')
            return render_template('resources/lenses/new.html', form=form)


@bp.route('/<lens_id>/edit', methods=['GET'])
@login_required
def edit(lens_id):
    lens = db.session.query(Lens).filter(Lens.id == lens_id).first()
    form = LensesForm()
    form.zoom.data = lens.zoom
    form.numerical_aperture.data = lens.numerical_aperture
    return render_template('resources/lenses/edit.html', form=form)


@bp.route('/<lens_id>/edit', methods=['POST'])
@login_required
def edit_post(lens_id):
    # convert request.form to form object
    form = LensesForm(request.form)
    if not form.validate():
        return render_template('resources/lenses/edit.html', form=form)
        # if the form is valid, create a new lens and redirect to the index page
    else:
        # if unique constraint is violated, inform the user
        try:
            lens = db.session.query(Lens).filter(Lens.id == lens_id).first()
            lens.zoom = form.zoom.data
            lens.numerical_aperture = form.numerical_aperture.data
            db.session.commit()
            return redirect(url_for('lenses.index'))
        except sqlalchemy.exc.IntegrityError:
            flash('Diese Kombination aus Zoom und numerischer Apertur existiert bereits', 'danger')
            return render_template('resources/lenses/edit.html', form=form)


@bp.route('/<lens_id>/delete')
@login_required
def delete(lens_id):
    try:
        lens = db.session.query(Lens).filter(Lens.id == lens_id).first()
        db.session.delete(lens)
        db.session.commit()
        flash("Objektiv wurde gelöscht", 'success')
        return redirect(url_for('lenses.index'))
    except sqlalchemy.exc.IntegrityError:
        flash('Dieses Objektiv wird noch verwendet und kann daher nicht gelöscht werden', 'danger')
        return redirect(url_for('lenses.index'))
    except:
        flash('Objektiv konnte nicht gelöscht werden. Probieren Sie es später erneut.', 'danger')
        return redirect(url_for('lenses.index'))
