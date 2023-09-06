import sqlalchemy.exc
from flask import render_template, request, url_for, flash, redirect
from app.spectra_types import bp
from app.models.model import SpectrumType
from app.extensions import db

