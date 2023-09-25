from functools import wraps

from flask import render_template, request, url_for, flash, redirect
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash

from app.extensions import db
from app.forms.forms import SignupForm
from app.models.model import Group, User
from app.routes.admin import bp

def admin_required(f):
    """
        Decorator for pages that require admin rights

    Args:
        f (callable): The original function to be decorated.

    Returns:
        callable: A wrapped function that checks if the user is an admin.
    """
    @wraps(f)
    def wrap(*args, **kwargs):
        group = db.session.query(Group).filter(Group.id == current_user.group_id).first()
        if group.name == "admin":
            return f(*args, **kwargs)
        else:
            flash("Sie haben keine Berechtigung für diese Seite.", "danger")
            return redirect(url_for('main.index'))

    return wrap



@bp.route('/new', methods=['GET'])
@login_required
@admin_required
def new():
    """
        Create page for users, only accessible for logged in users

    Returns:
        rendered template of the new page, with the form for creating a new user
    """
    form = SignupForm()
    return render_template('resources/auth/signup.html', form=form)


@bp.route('/new', methods=['POST'])
@login_required
@admin_required
def new_post():
    """
        Creates a new admin, only accessible for admins

    Returns:
        based on the validation of the form, either redirects to this resources index
        page or renders the Create page again with validation errors (WTForms) or integrity errors (SQL constraints)
    """

    # convert request.form to form object
    form = SignupForm(request.form)

    # check if the email already exists
    user = db.session.query(User).filter_by(email=form.email.data).first()
    if user:
        flash('Diese E-Mail-Adresse ist bereits vergeben', 'danger')
        form_ok = False
        return render_template('resources/auth/signup.html', form=form)

    # if the form is not valid, redirect to the signup page
    if not form.validate():
        return render_template('resources/auth/signup.html', form=form)

    # create a new user
    new_user = User(first_name=form.firstname.data, last_name=form.lastname.data, email=form.email.data,
                    password_hash=generate_password_hash(form.password.data, method='sha256'), group_id=1, active=True)

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    # send the user to the login page
    flash('Der Account wurde erfolgreich erstellt.',
          'success')
    return redirect(url_for('admin.index'))

@bp.route('/')
@login_required
@admin_required
def index():
    """
        Index page for admin, only accessible for logged in users. Allowing the admin to activate, deactivate and delete users

    Returns:
        rendered template of the index page, with all the users and their groups
    """
    users = db.session.query(User).all()
    groups = db.session.query(Group).all()
    return render_template('resources/admins/index.html', users=users, groups=groups)


@bp.route('/activate/<user_id>')
@login_required
@admin_required
def activate(user_id):
    """
        Activates a user by setting the active flag to True, only accessible for logged in users

    Args:
        user_id (int): id of the user to activate, passed as a url parameter

    Returns:
        redirects to the admin index page, with a flash message based on the success of the deletion
    """
    try:
        user = db.session.query(User).filter(User.id == user_id).first()
        if user.active:
            flash('User ist bereits aktiviert', 'danger')
            return redirect(url_for('admin.index'))
        user.active = True
        db.session.commit()
        flash('User wurde aktiviert', 'success')
        return redirect(url_for('admin.index'))
    except:
        flash('User konnte nicht aktiviert werden', 'danger')
        return redirect(url_for('admin.index'))


@bp.route('/deactivate/<user_id>')
@login_required
@admin_required
def deactivate(user_id):
    """
        Deactivates a user by setting the active flag to False, only accessible for logged in users

    Args:
        user_id (int): id of the user to deactivate, passed as a parameter in the url

    Returns:
        redirects to the admin index page, with a flash message based on the success of the deletion
    """
    try:
        user = db.session.query(User).filter(User.id == user_id).first()
        if not user.active:
            flash('User ist bereits deaktiviert', 'danger')
            return redirect(url_for('admin.index'))
        user.active = False
        db.session.commit()
        flash('User wurde deaktiviert', 'success')
        return redirect(url_for('admin.index'))
    except:
        flash('User konnte nicht deaktiviert werden', 'danger')
        return redirect(url_for('admin.index'))

@bp.route('/delete/<user_id>')
@login_required
@admin_required
def delete(user_id):
    """
        Deletes the user, only accessible for logged in users

    Args:
        user_id (int): id of the user to delete, passed as a url parameter

    Returns:
        redirects to the admin index page, with a flash message based on the success of the deletion
    """
    try:
        user = db.session.query(User).filter(User.id == user_id).first()
        db.session.delete(user)
        db.session.commit()
        flash('User wurde gelöscht', 'success')
        return redirect(url_for('admin.index'))
    except:
        flash('User konnte nicht gelöscht werden', 'danger')
        return redirect(url_for('admin.index'))
