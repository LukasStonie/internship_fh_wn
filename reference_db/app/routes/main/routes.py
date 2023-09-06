from flask import render_template
from app.routes.main import bp

@bp.route('/')
def index():
    return render_template('index.html')