from flask import Blueprint

bp = Blueprint('compounds', __name__)

from app.compounds import routes