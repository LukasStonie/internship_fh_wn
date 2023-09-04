from flask import Blueprint

bp = Blueprint('lenses', __name__)

from app.lenses import routes