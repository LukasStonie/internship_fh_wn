from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, IntegerField, BooleanField,
                     RadioField)
from wtforms.validators import InputRequired, Length, Email, EqualTo



class SignupForm(FlaskForm):
    firstname = StringField('Vorname', validators=[InputRequired(), Length(min=2, max=45)])
    lastname = StringField('Nachname', validators=[InputRequired(), Length(min=2, max=60)])
    email = StringField('E-Mail', validators=[InputRequired(), Length(min=2, max=60), Email()])
    password = StringField('Passwort', validators=[InputRequired(), Length(min=8, max=60), EqualTo('password_repeat',
                                                                                                   message='Passwörter stimmen nicht überein')])
    password_repeat = StringField('Passwort wiederholen',
                                  validators=[InputRequired(), Length(min=8, max=60)])


class LoginForm(FlaskForm):
    email = StringField('E-Mail', validators=[InputRequired(), Length(min=2, max=60), Email()])
    password = StringField('Passwort', validators=[InputRequired(), Length(min=8, max=60)])
