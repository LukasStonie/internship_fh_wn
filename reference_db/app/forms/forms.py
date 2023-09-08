from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, IntegerField, BooleanField,
                     RadioField, PasswordField)
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, Length, Email, EqualTo


class SignupForm(FlaskForm):
    firstname = StringField('Vorname', validators=[InputRequired(), Length(min=2, max=45)])
    lastname = StringField('Nachname', validators=[InputRequired(), Length(min=2, max=60)])
    email = EmailField('E-Mail', validators=[InputRequired(), Length(min=2, max=60), Email()])
    password = PasswordField('Passwort', validators=[
            InputRequired(),
        Length(min=8, max=60),
        EqualTo('password_repeat', message='Passwörter stimmen nicht überein')])
    password_repeat = PasswordField('Passwort wiederholen',
                                    validators=[InputRequired(), Length(min=8, max=60)])


class LoginForm(FlaskForm):
    email = EmailField('E-Mail', validators=[InputRequired(), Length(min=2, max=60), Email()])
    password = PasswordField('Passwort', validators=[InputRequired(), Length(min=8, max=60)])


class LensesForm(FlaskForm):
    zoom = IntegerField('Zoom', validators=[InputRequired() ])
    numerical_aperture = IntegerField('Numerische Apertur', validators=[InputRequired()])

class LasersForm(FlaskForm):
    wavelength = IntegerField('Wellenlänge [nm]', validators=[InputRequired()])
