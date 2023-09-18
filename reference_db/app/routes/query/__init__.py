from flask import Blueprint

bp = Blueprint('query', __name__)

from app.routes.query import routes