from flask import Blueprint

bp = Blueprint('spectra_types', __name__)

from app.routes.spectra_types import routes