from flask import Blueprint

bp = Blueprint('lenses', __name__)

from app.routes.lenses import routes