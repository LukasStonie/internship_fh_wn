from flask import Blueprint

bp = Blueprint('spectra_types', __name__)

from app.spectra_types import routes