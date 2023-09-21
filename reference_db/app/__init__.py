from flask import Flask
from config import Config
from app.extensions import db
from flask_babel import Babel


def create_app(config_class=Config):
    """
    Creates the flask app instance, initializes the extensions (flask_login, flask_babel, flask_wtforms)
    and registers the blueprints.

    Args:
        config_class (custom Config class):

    Returns:
        flask app instance used for starting the server
    """

    app = Flask(__name__)
    babel = Babel(app)
    app.config['BABEL_DEFAULT_LOCALE'] = 'de'
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    db.init_app(app)

    # csrf token for forms
    from app.extensions import csrf
    csrf.init_app(app)

    # user session management
    from flask_login import LoginManager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = "Sie müssen sich anmelden, um diese Seite zu sehen."
    login_manager.login_message_category = "danger"
    login_manager.init_app(app)

    from app.models.model import User
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(User).get(int(user_id))

    # Register blueprints here
    from app.routes.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.routes.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.routes.lenses import bp as lenses_bp
    app.register_blueprint(lenses_bp, url_prefix='/lenses')

    from app.routes.lasers import bp as lasers_bp
    app.register_blueprint(lasers_bp, url_prefix='/lasers')

    from app.routes.apertures import bp as apertures_bp
    app.register_blueprint(apertures_bp, url_prefix='/apertures')

    from app.routes.slides import bp as slides_bp
    app.register_blueprint(slides_bp, url_prefix='/slides')

    from app.routes.spectral_ranges import bp as spectral_ranges_bp
    app.register_blueprint(spectral_ranges_bp, url_prefix='/spectral_ranges')

    from app.routes.resolutions import bp as resolutions_bp
    app.register_blueprint(resolutions_bp, url_prefix='/resolutions')

    from app.routes.substrates import bp as substrates_bp
    app.register_blueprint(substrates_bp, url_prefix='/substrates')

    from app.routes.preprocessing_steps import bp as preprocessing_steps_bp
    app.register_blueprint(preprocessing_steps_bp, url_prefix='/preprocessing_steps')

    from app.routes.spectra_types import bp as spectrum_types_bp
    app.register_blueprint(spectrum_types_bp, url_prefix='/spectra_types')

    from app.routes.compounds import bp as compounds_bp
    app.register_blueprint(compounds_bp, url_prefix='/compounds')

    from app.routes.spectra import bp as spectra_bp
    app.register_blueprint(spectra_bp, url_prefix='/spectra')

    from app.routes.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    from app.routes.intensities import bp as intensities_bp
    app.register_blueprint(intensities_bp, url_prefix='/intensities')

    from app.routes.peaks import bp as peaks_bp
    app.register_blueprint(peaks_bp, url_prefix='/peaks')

    from app.routes.query import bp as query_bp
    app.register_blueprint(query_bp, url_prefix='/query')

    return app
