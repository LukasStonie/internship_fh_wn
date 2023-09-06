import sqlalchemy.exc
from flask import render_template, request, url_for, flash, redirect
from app.routes.slides import bp
from app.models.model import Slide
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
    slides = db.session.query(Slide).all()
    return render_template('resources/slides/index.html', slides=slides)


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
            return redirect(url_for('slides.new', name=name))
        # if the form is valid, create a new slide and redirect to the index page
        else:
            # if unique constraint is violated, inform the user
            try:
                slide = Slide(name=name)
                db.session.add(slide)
                db.session.commit()
                return redirect(url_for('slides.index'))
            except sqlalchemy.exc.IntegrityError:
                flash('Diese Bezeichnung existiert bereits', 'error')
                return redirect(url_for('slides.new', name=name))
    # if the request method is GET, the user wants to display the form
    else:
        return render_template('resources/slides/new.html', values=request.args)


@bp.route('/<slide_id>/edit', methods=['GET', 'POST'])
def edit(slide_id):
    # if the request method is POST, the form was submitted
    # validate the form and create a new slide
    if request.method == 'POST':
        # validate form
        # form_ok signifies if the form is valid or not
        # name is the value from the form
        form_ok, name = validate_form(request.form)
        # if the form is not valid, redirect to the new page and pass the values from the form
        if not form_ok:
            return redirect(url_for('slides.edit', slide_id=slide_id, name=name))
        # if the form is valid, create a new slide and redirect to the index page
        else:
            # if unique constraint is violated, inform the user
            try:
                slide = db.session.query(Slide).filter(Slide.id == slide_id).first()
                slide.name = name
                db.session.commit()
                return redirect(url_for('slides.index'))
            except sqlalchemy.exc.IntegrityError:
                flash('Diese Bezeichnung existiert bereits', 'error')
                return redirect(url_for('slides.edit', slide_id=slide_id, name=name))
    else:
        # if the request method is GET, the user wants to display the form
        # if request.args is empty, there was no attempt to submit the form
        # if request.args is not empty, the form was submitted but validation failed and the values from the form are passed
        args_len = len(request.args.keys())
        slide = vars(db.session.query(Slide).filter(Slide.id == slide_id).first()) \
            if args_len == 0 \
            else request.args
        return render_template('resources/slides/edit.html', slide=slide)


@bp.route('/<slide_id>/delete')
def delete(slide_id):
    slide = db.session.query(Slide).filter(Slide.id == slide_id).first()
    db.session.delete(slide)
    db.session.commit()
    return redirect(url_for('slides.index'))