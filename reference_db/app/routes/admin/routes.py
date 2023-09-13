from functools import wraps

from flask import render_template, request, url_for, flash, redirect
from flask_login import login_required, current_user
from app.extensions import db
from app.models.model import Group, User
from app.routes.admin import bp

def admin_required(f):
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
    users = db.session.query(User).all()
    groups = db.session.query(Group).all()
    return render_template('resources/admins/index.html', users=users, groups=groups)


@bp.route('/activate/<user_id>')
@login_required
@admin_required
def activate(user_id):
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
    try:
        user = db.session.query(User).filter(User.id == user_id).first()
        db.session.delete(user)
        db.session.commit()
        flash('User wurde gelöscht', 'success')
        return redirect(url_for('admin.index'))
    except:
        flash('User konnte nicht gelöscht werden', 'danger')
        return redirect(url_for('admin.index'))
