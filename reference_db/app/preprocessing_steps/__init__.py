from flask import Blueprint

bp = Blueprint('preprocessing_steps', __name__)

from app.preprocessing_steps import routes