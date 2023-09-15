from flask import Blueprint

bp = Blueprint('peaks', __name__)

from app.routes.peaks import routes