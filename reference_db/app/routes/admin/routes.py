from functools import wraps

from flask import render_template, request, url_for, flash, redirect
from flask_login import login_required, current_user
from app.extensions import db
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
