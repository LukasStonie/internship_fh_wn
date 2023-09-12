from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from app.business_logic import convert

import matplotlib.pyplot as plt

from flask_wtf import CSRFProtect

csrf = CSRFProtect()
