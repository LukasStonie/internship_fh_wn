from sqlalchemy import Table, Column, Integer, BLOB, String, ForeignKey, UniqueConstraint, BOOLEAN, \
    ForeignKeyConstraint, event, Float
from sqlalchemy.orm import declarative_base, relationship, backref
from flask_login import UserMixin
from sqlalchemy import event
from sqlalchemy.engine import Engine

import app

Base = declarative_base()

from sqlite3 import Connection as SQLite3Connection


@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()


class User(UserMixin, Base):
    """
        User model for the database, table-name: users

    Attributes:
        id (int): unique id for the user, pk

        first_name (str): first name of the user, nn

        last_name (str): last name of the user, nn

        email (str): email of the user, nn

        password_hash (str): hashed password of the user, nn

        group_id (int): id of the group the user belongs to, nn

        active (bool): whether the user is active or not, nn

    Constraints:
        email (str): unique email for the user
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(80), index=True, nullable=False)
    last_name = Column(String(80), index=True, nullable=False)
    email = Column(String(120), index=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    group_id = Column(Integer, nullable=False)
    active = Column(BOOLEAN, nullable=False)
    __table_args__ = (
        UniqueConstraint('email', name='u_email'),
    )

    def __repr__(self):
        return f'<User "{self.first_name}" "{self.last_name}" "{self.email}" "{self.active}">'


class Group(Base):
    """
        Group model for the database, table-name: groups

    Attributes:
        id (int): unique id for the group, pk

        name (str): name of the group, nn

    Constraints:
        name (str): unique name for the group
    """
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), index=True, nullable=False)
    __table_args__ = (
        UniqueConstraint('name', name='u_name'),
    )

    def __repr__(self):
        return f'<Group "{self.name}">'


class Substrate(Base):
    """
        Substrate model for the database, table-name: substrates

    Attributes:
        id (int): unique id for the substrate, pk

        name (str): name of the substrate, nn

        filename (str): name of the instruction file, nn

        instruction (str): instruction file

    Constraints:
        name (str): unique name for the substrate
    """
    __tablename__ = 'substrates'

    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    filename = Column(String(120), nullable=True)
    instruction = Column(BLOB, nullable=True)

    __table_args__ = (
        UniqueConstraint('name', name='u_name'),
    )

    def __repr__(self):
        return f'<Substrate "{self.name}">'


class Resolution(Base):
    """
        Resolution model for the database, table-name: resolutions

    Attributes:
        id (int): unique id for the resolution, pk

        description (str): description of the resolution, nn

    Constraints:
        description (str): unique description for the resolution
    """
    __tablename__ = 'resolutions'

    id = Column(Integer, primary_key=True)
    description = Column(String(64), nullable=False)

    __table_args__ = (
        UniqueConstraint('description', name='u_description'),
    )

    def __repr__(self):
        return f'<Resolution "{self.description}">'


class SpectralRange(Base):
    """
        SpectralRange model for the database, table-name: spectral_ranges

    Attributes:
        id (int): unique id for the spectral_range, pk

        start (int): start of the spectral_range, nn

        end (int): end of the spectral_range, nn

    Constraints:
        start (int) & end (int): unique start & end for the spectral_range
    """
    __tablename__ = 'spectral_ranges'

    id = Column(Integer, primary_key=True)
    start = Column(Integer, nullable=False)
    end = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint('start', 'end', name='u_start_end'),
    )

    def __repr__(self):
        return f'<SpectralRange "{self.start}" - "{self.end}">'


class Slide(Base):
    """
        Slide model for the database, table-name: slides

    Attributes:
        id (int): unique id for the slide, pk

        name (str): name of the slide, nn

    Constraints:
        name (str): unique name for the slide
    """
    __tablename__ = 'slides'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)

    __table_args__ = (
        UniqueConstraint('name', name='u_name'),
    )

    def __repr__(self):
        return f'<Slide "{self.name}">'


class Aperture(Base):
    """
        Aperture model for the database, table-name: apertures

    Attributes:
        id (int): unique id for the aperture, pk

        size (str): size of the aperture, nn

    Constraints:
        size (str): unique size for the aperture
    """
    __tablename__ = 'apertures'

    id = Column(Integer, primary_key=True)
    size = Column(String(20), nullable=False)

    __table_args__ = (
        UniqueConstraint('size', name='u_size'),
    )

    def __repr__(self):
        return f'<Aperture "{self.size}">'


class Laser(Base):
    """
        Laser model for the database, table-name: lasers

    Attributes:
        id (int): unique id for the laser, pk

        wavelength (int): wavelength of the laser, nn

    Constraints:
        wavelength (int): unique wavelength for the laser
    """
    __tablename__ = 'lasers'

    id = Column(Integer, primary_key=True)
    wavelength = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint('wavelength', name='u_wavelength'),
    )

    def __repr__(self):
        return f'<Laser "{self.wavelength}">'


class Lens(Base):
    """
        Lens model for the database, table-name: lenses

    Attributes:
        id (int): unique id for the lens, pk

        zoom (int): zoom of the lens, nn

        numerical_aperture (int): numerical aperture of the lens, nn

    Constraints:
        zoom (int) & numerical_aperture (int): unique zoom & numerical_aperture for the lens
    """
    __tablename__ = 'lenses'

    id = Column(Integer, primary_key=True)
    zoom = Column(Integer, nullable=False)
    numerical_aperture = Column(Integer, nullable=False)
    # UniqueConstraint('zoom', 'numerical_aperture', name='u_zoom_numerical_aperture')
    __table_args__ = (
        UniqueConstraint('zoom', 'numerical_aperture', name='u_zoom_numerical_aperture'),
    )

    def __repr__(self):
        return f'<Lens "{self.zoom}" - "{self.numerical_aperture}">'


spectrum_has_preprocessing_steps = Table('spectrum_has_preprocessing_steps', Base.metadata,
                                         Column("spectrum_id", ForeignKey('spectra.id')),
                                         Column("preprocessing_step_id",
                                                ForeignKey('preprocessing_steps.id', ondelete='RESTRICT')))


class Spectrum(Base):
    """
        Spectrum model for the database, table-name: spectra

    Attributes:
        id (int): unique id for the spectrum, pk

        file_path (str): path to the spectrum file, nn

        compound_id (int): id of the compound the spectrum belongs to, nn

        spectrum_type_id (int): id of the spectrum_type, nn

        spectrum_type (relationship): many-to-one

        preprocessing_steps (relationship): many-to-many

        peaks (relationship): one-to-many

    Constraints:
        file_path (str): unique file_path for the spectrum

    """
    __tablename__ = 'spectra'

    id = Column(Integer, primary_key=True)
    file_path = Column(String(200), nullable=False)
    compound_id = Column(Integer, ForeignKey('compounds.id'))
    spectrum_type_id = Column(Integer, ForeignKey('spectrum_types.id'), nullable=False)
    preprocessing_steps = relationship("PreprocessingSteps",
                                       secondary=spectrum_has_preprocessing_steps,
                                       back_populates="spectra")
    # block deletion of coresponding rows in other tables when used in a spectrum
    spectrum_type = relationship("SpectrumType", backref="spectra", passive_deletes='all')

    # delete all linked peaks when a spectrum is deleted
    peaks = relationship("Peak", backref="spectrum", cascade="all, delete-orphan")
    __table_args__ = (
        UniqueConstraint('file_path', name='u_file_path'),
    )

    def __repr__(self):
        return f'<Spectrum "{self.file_path}" - compound: "{self.compound_id}">'


class SpectrumType(Base):
    """
        SpectrumType model for the database, table-name: spectrum_types

    Attributes:
        id (int): unique id for the spectrum_type, pk

        name (str): name of the spectrum_type, nn

    Constraints:
        name (str): unique name for the spectrum_type
    """
    __tablename__ = 'spectrum_types'

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)

    __table_args__ = (
        UniqueConstraint('name', name='u_name'),
    )

    def __repr__(self):
        return f'<SpectrumType "{self.name}">'


class PreprocessingSteps(Base):
    """
        PreprocessingSteps model for the database, table-name: preprocessing_steps

    Attributes:
        id (int): unique id for the preprocessing_step, pk

        name (str): name of the preprocessing_step, nn

        spectra (relationship): many-to-many
    """
    __tablename__ = 'preprocessing_steps'

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    spectra = relationship("Spectrum",
                           secondary=spectrum_has_preprocessing_steps,
                           back_populates="preprocessing_steps")

    __table_args__ = (
        UniqueConstraint('name', name='u_name'),
    )

    def __repr__(self):
        return f'<PreprocessingSteps "{self.name}">'


class Intensity(Base):
    """
        Intensity model for the database, table-name: intensities

    Attributes:
        id (int): unique id for the intensity, pk

        shorthand (str): shorthand of the intensity, nn

        description (str): description of the intensity, nn

    Constraints:
        shorthand (str): unique shorthand for the intensity
    """
    __tablename__ = 'intensities'
    id = Column(Integer, primary_key=True)
    shorthand = Column(String(3), nullable=False)
    description = Column(String(15), nullable=False)

    __table_args__ = (
        UniqueConstraint('shorthand', name='u_shorthand'),
    )

    def __repr__(self):
        return f'<Intensity {self.shorthand}: {self.description}>'


class Peak(Base):
    """
        Peak model for the database, table-name: peaks

    Attributes:
        id (int): unique id for the peak, pk

        spectrum_id (int): id of the spectrum the peak belongs to, nn

        wavenumber (float): wavenumber of the peak, nn

        intensity_id (int): id of the intensity-classification, nn

        intensity (relationship): one-to-one
    """
    __tablename__ = 'peaks'
    id = Column(Integer, primary_key=True)
    spectrum_id = Column(Integer, ForeignKey('spectra.id'), nullable=False)
    wavenumber = Column(Float, nullable=False)
    intensity_id = Column(Integer, ForeignKey('intensities.id'), nullable=False)

    # spectrum = relationship("Spectrum", backref="peaks",)
    intensity = relationship("Intensity", backref="peaks")

    __table_args__ = (
        UniqueConstraint('spectrum_id', 'wavenumber', name='u_spectrum_id_wavenumber'),
    )

    def __repr__(self):
        return f'<Peak {self.wavenumber} {self.intensity_id}>'


class Compound(Base):
    """
        Compound model for the database, table-name: compounds

    Attributes:
        id (int): unique id for the compound, pk

        name (str): name of the compound, nn

        coaddition (int): coaddition of the compound, nn

        integration_time (int): integration_time of the compound, nn

        lens_id (int): id of the lens, nn

        laser_id (int): id of the laser, nn

        laser_power (int): power of the laser, nn

        spectral_range_id (int): id of the spectral_range, nn

        resolution_id (int): id of the resolution, nn

        aperture_id (int): id of the aperture, nn

        slide_id (int): id of the slide, nn

        substrate_id (int): id of the substrate, nn

        user (str): user who created the compound, nn

        description (str): description of the compound

        date (str): date the compound was created, nn

        spectra (relationship): one-to-many

        lens (relationship): one-to-one

        laser (relationship): one-to-one

        spectral_range (relationship): one-to-one

        resolution (relationship): one-to-one

        slide (relationship): one-to-one

        aperture (relationship): one-to-one

        substrate (relationship): one-to-one

    Constraints:
        name (str): unique name for the compound
    """
    __tablename__ = 'compounds'

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    coaddition = Column(Integer, nullable=False)
    integration_time = Column(Integer, nullable=False)
    lens_id = Column(Integer, ForeignKey('lenses.id'), nullable=False)
    laser_id = Column(Integer, ForeignKey('lasers.id'), nullable=False)
    laser_power = Column(Integer, nullable=False)
    spectral_range_id = Column(Integer, ForeignKey('spectral_ranges.id'), nullable=False)
    resolution_id = Column(Integer, ForeignKey('resolutions.id'), nullable=False)
    aperture_id = Column(Integer, ForeignKey('apertures.id'), nullable=False)
    slide_id = Column(Integer, ForeignKey('slides.id'), nullable=False)
    substrate_id = Column(Integer, ForeignKey('substrates.id', ondelete='RESTRICT'), nullable=True)
    user = Column(String(200), nullable=False)
    description = Column(String(400), nullable=True)
    date = Column(String(15), nullable=False)

    spectra = relationship("Spectrum", backref="compound", cascade="all, delete")

    # block deletion of coresponding rows in other tables when used in a compound
    lens = relationship("Lens", backref="compound", passive_deletes='all')
    laser = relationship("Laser", backref="compound", passive_deletes='all')
    spectral_range = relationship("SpectralRange", backref="compound", passive_deletes='all')
    resolution = relationship("Resolution", backref="compound", passive_deletes='all')
    slide = relationship("Slide", backref="compound", passive_deletes='all')
    aperture = relationship("Aperture", backref="compound", passive_deletes='all')

    substrate = relationship("Substrate", backref="compound")

    __table_args__ = (
        UniqueConstraint('name', name='u_name'),
    )

    def __repr__(self):
        return f'<Compound "{self.name}">'


with app.create_app().app_context():
    # Base.metadata.drop_all(app.db.engine)
    Base.metadata.create_all(app.db.engine)
