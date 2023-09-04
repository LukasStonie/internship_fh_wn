from flask import render_template
from app.lenses import bp
from app.models.model import Lens
from app.extensions import db


@bp.route('/')
def index():
    # get all lenses from database using SQLAlchemy and pass them to the template
    lenses = db.session.query(Lens).all()
    lenses = []
    return render_template('lenses/index.html', lenses=lenses)

@bp.route('/<lens_id>')
def show(lens_id):
    return render_template('lenses/show.html', lens_id=lens_id)

@bp.route('/<lens_id>/edit')
def edit(lens_id):
    return render_template('lenses/edit.html', lens_id=lens_id)

@bp.route('/<lens_id>/delete')
def delete(lens_id):
    return render_template('lenses/delete.html', lens_id=lens_id)

@bp.route('/new')
def new():
    return render_template('lenses/new.html')