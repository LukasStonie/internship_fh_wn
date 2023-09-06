from flask import Blueprint

bp = Blueprint('apertures', __name__)

from app.routes.apertures import routes