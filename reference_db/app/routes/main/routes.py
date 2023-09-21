from flask import render_template
from app.routes.main import bp
from flask_login import login_required, current_user


@bp.route('/')
def index():
    """
        Start page for the application, accessible for all users

    Returns:
        rendered template of the start page
    """
    return render_template('index.html', name=current_user)
