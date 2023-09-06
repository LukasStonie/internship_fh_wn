from flask import Blueprint

bp = Blueprint('spectra', __name__)

from app.spectra import routes