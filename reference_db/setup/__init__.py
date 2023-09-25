"""
    This package contains the setup files for the project.

    The files in this package are used to setup the project, e.g. create the admin user, the user groups
    and create the necessary spectra_types since they are referenced in the code.

    The files in this package are not used during runtime of the application.
"""
from setup.setup import run_setup

run_setup()
