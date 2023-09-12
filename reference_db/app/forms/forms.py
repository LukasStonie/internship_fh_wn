from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import (StringField, TextAreaField, IntegerField, BooleanField,
                     RadioField, PasswordField, SelectField, SelectMultipleField, SubmitField)
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
    zoom = IntegerField('Zoom', validators=[InputRequired(message="Bitte geben Sie eine Vergößerung ein")])
    numerical_aperture = IntegerField('Numerische Apertur',
                                      validators=[InputRequired(message="Bitte geben Sie eine numerische Apertur ein")])


class LasersForm(FlaskForm):
    wavelength = IntegerField('Wellenlänge [nm]',
                              validators=[InputRequired(message='Bitte geben Sie eine Wellenlänge an')])


class AperturesForm(FlaskForm):
    size = IntegerField('Größe [µm]', validators=[InputRequired(message='Bitte geben Sie eine Größe an')])


class SlidesForm(FlaskForm):
    name = StringField('Bezeichnung', validators=[InputRequired(message='Bitte geben Sie eine Bezeichnung an')])


class SpectralRangesForm(FlaskForm):
    start = IntegerField(label="Start [cm<sup>-1</sup>]",
                         validators=[InputRequired(message='Bitte geben Sie einen Startwert an')])
    end = IntegerField('Ende [cm^-1]', validators=[InputRequired(message='Bitte geben Sie einen Endwert an')])


class ResolutionsForm(FlaskForm):
    description = StringField('Bezeichnung', validators=[InputRequired(message='Bitte geben Sie eine Bezeichnung an')])


class SpectralTypesForm(FlaskForm):
    description = StringField('Bezeichnung', validators=[InputRequired(message='Bitte geben Sie eine Bezeichnung an')])


class PreprocessingStepsForm(FlaskForm):
    name = StringField('Bezeichnung', validators=[InputRequired(message='Bitte geben Sie eine Bezeichnung an')])


class SubstratesForm(FlaskForm):
    name = StringField('Bezeichnung', validators=[InputRequired(message='Bitte geben Sie eine Bezeichnung an')])
    instructions = FileField('Anleitung', validators=[])


class CompoundsForm(FlaskForm):
    name = StringField('Bezeichnung', validators=[InputRequired(message='Bitte geben Sie eine Bezeichnung an')])
    coaddition = IntegerField('Koaddition', validators=[InputRequired(message='Bitte geben Sie eine Koaddition an')])
    integration_time = IntegerField('Integrationszeit [ms]',
                                    validators=[InputRequired(message='Bitte geben Sie eine Integrationszeit an')])
    laser_power = IntegerField('Laserleistung [mW]',
                               validators=[InputRequired(message='Bitte geben Sie eine Laserleistung an')])
    description = StringField('Beschreibung', validators=[])

    lenses = SelectField('Objektiv', validate_choice=False,
                         validators=[InputRequired(message='Bitte wählen Sie ein Objektiv aus')])
    lasers = SelectField('Laser', validate_choice=False,
                         validators=[InputRequired(message='Bitte wählen Sie einen Laser aus')])
    apertures = SelectField('Blende [µm]', validate_choice=False,
                            validators=[InputRequired(message='Bitte wählen Sie eine Blende aus')])
    slides = SelectField('Objektträger', validate_choice=False,
                         validators=[InputRequired(message='Bitte wählen Sie einen Objektträger aus')])
    spectral_ranges = SelectField('Spektralbereich', validate_choice=False,
                                  validators=[InputRequired(message='Bitte wählen Sie einen Spektralbereich aus')])
    resolutions = SelectField('Auflösung', validate_choice=False,
                              validators=[InputRequired(message='Bitte wählen Sie eine Auflösung aus')])
    substrates = SelectField('Substrat', validate_choice=False, validators=[])

    create = SubmitField('Erstellen')
    create_and_add = SubmitField('Erstellen und Spektrum hinzufügen')


class SpectraForm(FlaskForm):
    spectrum_type = RadioField('Spektrumart', validate_choice=False,
                               validators=[InputRequired(message='Bitte wählen Sie einen Spektrumtyp aus')])
    preprocessing_steps = SelectMultipleField('Vorverarbeitung', validate_choice=False, validators=[])


class SpectraEditForm(FlaskForm):
    spectrum_type = RadioField('Spektrumart', validate_choice=False,
                               validators=[InputRequired(message='Bitte wählen Sie einen Spektrumtyp aus')])
    preprocessing_steps = SelectMultipleField('Vorverarbeitung', validate_choice=False, validators=[])
    new_spectrum = BooleanField('Spektrum austauschen')