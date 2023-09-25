import sqlalchemy.exc
from werkzeug.security import generate_password_hash

from app import create_app
from app import db
from app.models.model import User, SpectrumType, Group


def create_admin():
    """
        Creates the admin user with the username 'admin' and the password 'admin'

    Returns:
        None
    """
    try:
        # create the admin user with the username 'admin' and the password 'surfaceenhanced'
        # the password is hashed with the sha256 algorithm
        # the admin user is assigned to the admin group
        # the admin user is active
        admin = User(first_name='admin', last_name='admin', email='admin@refdb.at',
                     password_hash=generate_password_hash('surfaceenhanced', method='sha256'),
                     group_id=1, active=True)
        db.session.add(admin)
        db.session.commit()
        print("Admin created")
    except sqlalchemy.exc.IntegrityError:
        print("Admin already exists")
    except Exception as e:
        print("Error while creating admin")
        print(e)


def create_user_groups():
    """
        Creates the user groups 'admin' and 'user'

    Returns:
        None
    """
    try:
        # create the user groups 'admin' and 'user'
        admin = Group(name='admin')
        db.session.add(admin)

        user = Group(name='user')
        db.session.add(user)

        db.session.commit()
        print("User groups created")
    except sqlalchemy.exc.IntegrityError:
        print("tried to create user groups (admin, user), but at least one of them already exist")
    except Exception as e:
        print("Error while creating user groups")
        print(e)


def create_spectrum_types():
    """
        Creates the spectrum types 'roh', 'vorverarbeitet' and 'nur Peaks'

    Returns:
        None
    """
    try:
        # create the spectrum types 'roh', 'vorverarbeitet' and 'nur Peaks'
        raw = SpectrumType(name='roh')
        db.session.add(raw)

        preprocessed = SpectrumType(name='vorverarbeitet')
        db.session.add(preprocessed)

        peak = SpectrumType(name='nur Peaks')
        db.session.add(peak)

        db.session.commit()
        print("Spectrum types created")
    except sqlalchemy.exc.IntegrityError:
        print("tried to create spectrum types, but at least one of them already exist")
    except Exception as e:
        print("Error while creating spectrum types")
        print(e)


def run_setup():
    """
        Runs the setup for the project

    Returns:
        None
    """
    with create_app().app_context():
        db.create_all()
        create_user_groups()
        create_admin()
        create_spectrum_types()


if __name__ == '__main__':
    run_setup()
