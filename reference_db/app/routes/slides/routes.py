import sqlalchemy.exc
from flask import render_template, request, url_for, flash, redirect
from flask_login import login_required

from app.forms.forms import SlidesForm
from app.routes.slides import bp
from app.models.model import Slide
from app.extensions import db


@bp.route('/')
@login_required
def index():
    """
        Index page for slides, only accessible for logged in users. Allowing the user to add, edit and delete slides
        
    Returns:
        rendered template of the index page, with all the slides
        allowing the user to add, edit and delete slides
    """
    slides = db.session.query(Slide).all()
    return render_template('resources/slides/index.html', slides=slides)


@bp.route('/new', methods=['GET'])
@login_required
def new():
    """
        Create page for slides, only accessible for logged in users
        
    Returns:
        rendered template of the new page, with the form for creating a new slide
    """
    form = SlidesForm()
    return render_template('resources/slides/new.html', form=form)


@bp.route('/new', methods=['POST'])
@login_required
def new_post():
    """
        Creates a new slide if form is valid, only accessible for logged in users
        
    Returns:
        based on the validation of the form, either redirects to this resources index page or 
        renders the Create page again with validation errors (WTForms) or integrity errors (SQL constraints)
    """
    # convert request.form to form object
    form = SlidesForm(request.form)
    # if the form is not valid, redirect to the new page and pass the values from the form
    if not form.validate():
        return render_template('resources/slides/new.html', form=form)
    # if the form is valid, create a new slide and redirect to the index page
    else:
        # if unique constraint is violated, inform the user
        try:
            slide = Slide(name=form.name.data)
            db.session.add(slide)
            db.session.commit()
            return redirect(url_for('slides.index'))
        except sqlalchemy.exc.IntegrityError:
            flash('Diese Bezeichnung existiert bereits', 'danger')
            return render_template('resources/slides/new.html', form=form)


@bp.route('/<slide_id>/edit', methods=['GET'])
@login_required
def edit(slide_id):
    """
        Edit page for slides, only accessible for logged in users
        
    Args:
        slide_id (int): id of the slide to be edited

    Returns:
        rendered template of the edit page, with all the slides
    """
    slide = db.session.query(Slide).filter(Slide.id == slide_id).first()
    form = SlidesForm(obj=slide)
    return render_template('resources/slides/edit.html', form=form)


@bp.route('/<slide_id>/edit', methods=['POST'])
@login_required
def edit_post(slide_id):
    """
        Edits the slide if form is valid, only accessible for logged in users
        
    Args:
        slide_id (int): id of the slide to be edited

    Returns:
        based on the validation of the form, either redirects to this resources index page or 
        renders the Edit page again with validation errors (WTForms) or integrity errors (SQL constraints)
    """
    # convert request.form to form object
    form = SlidesForm(request.form)
    # if the form is not valid, redirect to the new page and pass the values from the form
    if not form.validate():
        return render_template('resources/slides/edit.html', form=form)
    # if the form is valid, create a new slide and redirect to the index page
    else:
        # if unique constraint is violated, inform the user
        try:
            slide = db.session.query(Slide).filter(Slide.id == slide_id).first()
            slide.name = form.name.data
            db.session.commit()
            return redirect(url_for('slides.index'))
        except sqlalchemy.exc.IntegrityError:
            flash('Diese Bezeichnung existiert bereits', 'danger')
            return render_template('resources/slides/edit.html', form=form)


@bp.route('/<slide_id>/delete')
@login_required
def delete(slide_id):
    """
        Deletes the slide if not used in a compound, only accessible for logged in users
        
    Args:
        slide_id (int): id of the slide to be deleted

    Returns:
        redirects to the index page with flash message based on the success of the deletion
    """
    try:
        slide = db.session.query(Slide).filter(Slide.id == slide_id).first()
        db.session.delete(slide)
        db.session.commit()
        flash("Objektträger wurde gelöscht", 'success')
        return redirect(url_for('slides.index'))
    except sqlalchemy.exc.IntegrityError:
        flash("Dieser Objektträger wird noch verwendet und konnte daher nicht gelöscht werden", 'danger')
        return redirect(url_for('slides.index'))
    except:
        flash("Objektträger konnte nicht gelöscht werden", 'danger')
        return redirect(url_for('slides.index'))
