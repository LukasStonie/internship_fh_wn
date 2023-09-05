from flask import Blueprint

bp = Blueprint('lasers', __name__)

from app.lasers import routes
