from flask import Blueprint

bp = Blueprint('substrates', __name__)

from app.substrates import routes