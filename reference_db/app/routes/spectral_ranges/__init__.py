from flask import Blueprint

bp = Blueprint('spectral_ranges', __name__)

from app.routes.spectral_ranges import routes