from sqlalchemy import Table, Column, Integer, BLOB, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

import app

Base = declarative_base()


class Substrate(Base):
    __tablename__ = 'substrates'

    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    instruction = Column(BLOB, nullable=True)

    def __repr__(self):
        return f'<Substrate "{self.material}">'


class Resolution(Base):
    __tablename__ = 'resolutions'

    id = Column(Integer, primary_key=True)
    resolution_description = Column(String(64), nullable=False)

    def __repr__(self):
        return f'<Resolution "{self.resolution}">'


class SpectralRange(Base):
    __tablename__ = 'spectral_ranges'

    id = Column(Integer, primary_key=True)
    start = Column(Integer, nullable=False)
    end = Column(Integer, nullable=False)

    def __repr__(self):
        return f'<SpectralRange "{self.start}" - "{self.end}">'


class Slide(Base):
    __tablename__ = 'slides'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)

    def __repr__(self):
        return f'<Slide "{self.name}">'


class Aperture(Base):
    __tablename__ = 'apertures'

    id = Column(Integer, primary_key=True)
    size = Column(Integer, nullable=False)

    def __repr__(self):
        return f'<Aperture "{self.size}">'


class Laser(Base):
    __tablename__ = 'lasers'

    id = Column(Integer, primary_key=True)
    wavelength = Column(Integer, nullable=False)

    def __repr__(self):
        return f'<Laser "{self.wavelength}">'


class Lens(Base):
    __tablename__ = 'lenses'

    id = Column(Integer, primary_key=True)
    zoom = Column(Integer, nullable=False)
    numerical_aperture = Column(Integer, nullable=False)

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

    def __repr__(self):
        return f'<Spectrum "{self.name}">'


class SepctrumType(Base):
    __tablename__ = 'spectrum_types'

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)

    def __repr__(self):
        return f'<SpectrumType "{self.name}">'


class PreprocessingSteps(Base):
    __tablename__ = 'preprocessing_steps'

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    description = Column(String(200), nullable=False)

    def __repr__(self):
        return f'<PreprocessingSteps "{self.name}">'


class Compound(Base):
    __tablename__ = 'compounds'

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    coaddition = Column(Integer, nullable=False)
    integration_time = Column(Integer, nullable=False)
    lens_id = Column(Integer, ForeignKey('lenses.id'))
    laser_id = Column(Integer, ForeignKey('lasers.id'))
    aperture_id = Column(Integer, ForeignKey('apertures.id'))
    slide_id = Column(Integer, ForeignKey('slides.id'))
    spectral_range_id = Column(Integer, ForeignKey('spectral_ranges.id'))
    resolution_id = Column(Integer, ForeignKey('resolutions.id'))
    substrate_id = Column(Integer, ForeignKey('substrates.id'))

    def __repr__(self):
        return f'<Compound "{self.name}">'

"""with app.create_app().app_context():
    Base.metadata.drop_all(app.db.engine)
    Base.metadata.create_all(app.db.engine)"""