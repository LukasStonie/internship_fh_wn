from flask import Blueprint

bp = Blueprint('spectra', __name__)

from app.routes.spectra import routes