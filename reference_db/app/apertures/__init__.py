from flask import Blueprint

bp = Blueprint('apertures', __name__)

from app.apertures import routes