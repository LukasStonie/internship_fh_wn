"""
    Forms Module
"""

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import (StringField, TextAreaField, IntegerField, BooleanField,
                     RadioField, PasswordField, SelectField, SelectMultipleField, SubmitField, FieldList, FormField)
from wtforms.fields.html5 import EmailField, DecimalField
from wtforms.validators import InputRequired, Length, Email, EqualTo
from app.extensions import db


class SignupForm(FlaskForm):
    """
        WTForms class for the signup form

    Attributes:
        firstname: StringField, required, min 2, max 45

        lastname: StringField, required, min 2, max 60

        email: EmailField, required, min 2, max 60, email

        password: PasswordField, required, min 8, max 60, equal to password_repeat

        password_repeat: PasswordField, required, min 8, max 60
    """

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
    """
        WTForms class for the login form

    Attributes:
        email: EmailField, required, min 2, max 60, email

        password: PasswordField, required, min 8, max 60
    """
    email = EmailField('E-Mail', validators=[InputRequired(), Length(min=2, max=60), Email()])
    password = PasswordField('Passwort', validators=[InputRequired(), Length(min=8, max=60)])


class LensesForm(FlaskForm):
    """
        WTForms class for the lenses form

    Attributes:
        zoom: IntegerField, required

        numerical_aperture: IntegerField, required
    """
    zoom = IntegerField('Zoom', validators=[InputRequired(message="Bitte geben Sie eine Vergößerung ein")])
    numerical_aperture = IntegerField('Numerische Apertur',
                                      validators=[InputRequired(message="Bitte geben Sie eine numerische Apertur ein")])


class LasersForm(FlaskForm):
    """
        WTForms class for the lasers form

    Attributes:
        wavelength: IntegerField, required
    """
    wavelength = IntegerField('Wellenlänge [nm]',
                              validators=[InputRequired(message='Bitte geben Sie eine Wellenlänge an')])


class AperturesForm(FlaskForm):
    """
        WTForms class for the apertures form

    Attributes:
        size: IntegerField, required
    """
    size = IntegerField('Größe [µm]', validators=[InputRequired(message='Bitte geben Sie eine Größe an')])


class SlidesForm(FlaskForm):
    """
        WTForms class for the slides form

    Attributes:
        name: StringField, required
    """
    name = StringField('Bezeichnung', validators=[InputRequired(message='Bitte geben Sie eine Bezeichnung an')])


class SpectralRangesForm(FlaskForm):
    """
        WTForms class for the spectral_ranges form

    Attributes:
        start: IntegerField, required

        end: IntegerField, required
    """
    start = IntegerField(label="Start [cm<sup>-1</sup>]",
                         validators=[InputRequired(message='Bitte geben Sie einen Startwert an')])
    end = IntegerField('Ende [cm^-1]', validators=[InputRequired(message='Bitte geben Sie einen Endwert an')])


class ResolutionsForm(FlaskForm):
    """
        WTForms class for the resolutions form

    Attributes:
        description: IntegerField, required
    """
    description = StringField('Bezeichnung', validators=[InputRequired(message='Bitte geben Sie eine Bezeichnung an')])


class SpectralTypesForm(FlaskForm):
    """
        WTForms class for the spectral_types form

    Attributes:
        description: StringField, required
    """
    description = StringField('Bezeichnung', validators=[InputRequired(message='Bitte geben Sie eine Bezeichnung an')])


class PreprocessingStepsForm(FlaskForm):
    """
        WTForms class for the preprocessing_steps form

    Attributes:
        name: StringField, required
    """
    name = StringField('Bezeichnung', validators=[InputRequired(message='Bitte geben Sie eine Bezeichnung an')])


class SubstratesForm(FlaskForm):
    """
        WTForms class for the substrates form

    Attributes:
        name: StringField, required

        instructions: FileField, optional
    """
    name = StringField('Bezeichnung', validators=[InputRequired(message='Bitte geben Sie eine Bezeichnung an')])
    instructions = FileField('Anleitung', validators=[])


class CompoundsForm(FlaskForm):
    """
        WTForms class for the compounds form

    Attributes:
        name: StringField, required

        coaddition: IntegerField, required

        integration_time: IntegerField, required

        laser_power: IntegerField, required

        description: StringField, optional

        lenses: SelectField, required

        lasers: SelectField, required

        apertures: SelectField, required

        slides: SelectField, required

        spectral_ranges: SelectField, required

        resolutions: SelectField, required

        substrates: SelectField, optional

        create: SubmitField

        create_and_add: SubmitField, used to distinguish between create and create_and_add_spectrum
    """
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
    apertures = SelectField('Apertur [µm]', validate_choice=False,
                            validators=[InputRequired(message='Bitte wählen Sie eine Apertur aus')])
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
    """
        WTForms class for the spectra form

    Attributes:
        spectrum_type: RadioField, required

        preprocessing_steps: SelectMultipleField, optional
    """
    spectrum_type = RadioField('Spektrumart', validate_choice=False,
                               validators=[InputRequired(message='Bitte wählen Sie einen Spektrumtyp aus')])
    preprocessing_steps = SelectMultipleField('Vorverarbeitung', validate_choice=False, validators=[])


class SpectraEditForm(FlaskForm):
    """
        WTForms class for the spectra form

    Attributes:
        spectrum_type: RadioField, required

        preprocessing_steps: SelectMultipleField, optional

        new_spectrum: BooleanField, indicate if a new spectrum should be uploaded
    """
    spectrum_type = RadioField('Spektrumart', validate_choice=False,
                               validators=[InputRequired(message='Bitte wählen Sie einen Spektrumtyp aus')])
    preprocessing_steps = SelectMultipleField('Vorverarbeitung', validate_choice=False, validators=[])
    new_spectrum = BooleanField('Spektrum austauschen')


class IntensityForm(FlaskForm):
    """
        WTForms class for the intensities form

    Attributes:
        shorthand: StringField, required, min 1, max 3

        description: StringField, required
    """
    shorthand = StringField('Kürzel', validators=[InputRequired(message='Bitte geben Sie ein Kürzel an'),
                                                  Length(min=1, max=3,
                                                         message="Das Kürzel darf maximal drei Zeichen lang sein")])
    description = StringField('Beschreibung',
                              validators=[InputRequired(message='Bitte geben Sie eine Beschreibung an')])



class PeakForm(FlaskForm):
    """
        WTForms class for the peaks form

    Attributes:
        intensity: SelectField, required
    """
    intensities = SelectField("Intensität", validate_choice=False,
                              validators=[InputRequired(message="Bitte wählen Sie eine Intesität aus.")])


class QueryForm(FlaskForm):
    """
        WTForms class for the query form

    Attributes:
        tolerance: DecimalField, required, default 10.0
    """
    tolerance = DecimalField("Toleranz", default=10.0,
                             validators=[InputRequired(message="Bitte geben Sie einen Toleranzbereich an.")])
