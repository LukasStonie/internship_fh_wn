from flask import Blueprint

bp = Blueprint('resolutions', __name__)

from app.routes.resolutions import routes