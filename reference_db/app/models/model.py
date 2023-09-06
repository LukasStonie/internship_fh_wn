from sqlalchemy import Table, Column, Integer, BLOB, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship

import app

Base = declarative_base()


class Substrate(Base):
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
    __tablename__ = 'resolutions'

    id = Column(Integer, primary_key=True)
    description = Column(String(64), nullable=False)

    __table_args__ = (
        UniqueConstraint('description', name='u_description'),
    )

    def __repr__(self):
        return f'<Resolution "{self.description}">'


class SpectralRange(Base):
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
    __tablename__ = 'slides'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)

    __table_args__ = (
        UniqueConstraint('name', name='u_name'),
    )

    def __repr__(self):
        return f'<Slide "{self.name}">'


class Aperture(Base):
    __tablename__ = 'apertures'

    id = Column(Integer, primary_key=True)
    size = Column(Integer, nullable=False) #TODO make this a string

    __table_args__ = (
        UniqueConstraint('size', name='u_size'),
    )

    def __repr__(self):
        return f'<Aperture "{self.size}">'


class Laser(Base):
    __tablename__ = 'lasers'

    id = Column(Integer, primary_key=True)
    wavelength = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint('wavelength', name='u_wavelength'),
    )

    def __repr__(self):
        return f'<Laser "{self.wavelength}">'


class Lens(Base):
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
                                         Column("preprocessing_step_id", ForeignKey('preprocessing_steps.id')))


class Spectrum(Base):
    __tablename__ = 'spectra'

    id = Column(Integer, primary_key=True)
    file_path = Column(String(200), nullable=False)
    compound_id = Column(Integer, ForeignKey('compounds.id'))
    spectrum_type_id = Column(Integer, ForeignKey('spectrum_types.id'))
    preprocessing_steps = relationship("PreprocessingSteps", secondary=spectrum_has_preprocessing_steps)

    __table_args__ = (
        UniqueConstraint('file_path', name='u_file_path'),
    )

    def __repr__(self):
        return f'<Spectrum "{self.name}">'


class SpectrumType(Base):
    __tablename__ = 'spectrum_types'

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)

    __table_args__ = (
        UniqueConstraint('name', name='u_name'),
    )

    def __repr__(self):
        return f'<SpectrumType "{self.name}">'


class PreprocessingSteps(Base):
    __tablename__ = 'preprocessing_steps'

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)

    __table_args__ = (
        UniqueConstraint('name', name='u_name'),
    )

    def __repr__(self):
        return f'<PreprocessingSteps "{self.name}">'


class Compound(Base):
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
    substrate_id = Column(Integer, ForeignKey('substrates.id'), nullable=True)
    user = Column(String(200), nullable=False)
    description = Column(String(400), nullable=True)
    date = Column(String(15), nullable=False)

    def __repr__(self):
        return f'<Compound "{self.name}">'


"""with app.create_app().app_context():
    Base.metadata.drop_all(app.db.engine)
    Base.metadata.create_all(app.db.engine)"""