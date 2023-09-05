from flask import Flask, render_template, request, url_for, flash, redirect
from config import Config
from app.extensions import db



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    db.init_app(app)

    # Register blueprints here
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.lenses import bp as lenses_bp
    app.register_blueprint(lenses_bp, url_prefix='/lenses')

    from app.lasers import bp as lasers_bp
    app.register_blueprint(lasers_bp, url_prefix='/lasers')

    from app.apertures import bp as apertures_bp
    app.register_blueprint(apertures_bp, url_prefix='/apertures')

    from app.slides import bp as slides_bp
    app.register_blueprint(slides_bp, url_prefix='/slides')

    from app.spectral_ranges import bp as spectral_ranges_bp
    app.register_blueprint(spectral_ranges_bp, url_prefix='/spectral_ranges')

    from app.resolutions import bp as resolutions_bp
    app.register_blueprint(resolutions_bp, url_prefix='/resolutions')

    from app.substrates import bp as substrates_bp
    app.register_blueprint(substrates_bp, url_prefix='/substrates')

    from app.preprocessing_steps import bp as preprocessing_steps_bp
    app.register_blueprint(preprocessing_steps_bp, url_prefix='/preprocessing_steps')

    from app.spectra_types import bp as spectrum_types_bp
    app.register_blueprint(spectrum_types_bp, url_prefix='/spectra_types')

    @app.route('/test/')
    def test_page():
        return '<h1>Testing the Flask Application Factory Pattern</h1>'

    return app
