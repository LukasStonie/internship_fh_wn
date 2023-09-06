from flask import Blueprint

bp = Blueprint('preprocessing_steps', __name__)

from app.routes.preprocessing_steps import routes