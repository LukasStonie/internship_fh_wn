from flask import Blueprint

bp = Blueprint('resolutions', __name__)

from app.resolutions import routes