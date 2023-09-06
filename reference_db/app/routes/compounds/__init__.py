from flask import Blueprint

bp = Blueprint('compounds', __name__)

from app.routes.compounds import routes