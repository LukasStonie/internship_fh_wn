from flask import Blueprint

bp = Blueprint('spectral_ranges', __name__)

from app.spectral_ranges import routes