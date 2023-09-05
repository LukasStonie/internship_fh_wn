from flask import Blueprint

bp = Blueprint('slides', __name__)

from app.slides import routes