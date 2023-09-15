from flask import Blueprint

bp = Blueprint('intensities', __name__)

from app.routes.intensities import routes