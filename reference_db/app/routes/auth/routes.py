from flask import render_template, request, url_for, flash, redirect

from app.forms.forms import SignupForm, LoginForm
from app.routes.auth import bp
from app.models.model import User, Group
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required


@bp.route('/signup/', methods=['GET'])
def signup():
    form = SignupForm()
    return render_template('resources/auth/signup.html', form=form)


@bp.route('/signup/', methods=['POST'])
def signup_post():
    # convert request.form to form object
    form = SignupForm(request.form)

    # check if the email already exists
    user = db.session.query(User).filter_by(email=form.email.data).first()
    if user:
        flash('Diese E-Mail-Adresse ist bereits vergeben', 'danger')
        form_ok = False
        return render_template('resources/auth/signup.html', form=form)

    # if the form is not valid, redirect to the signup page
    if not form.validate():
        return render_template('resources/auth/signup.html', form=form)

    # create a new user
    new_user = User(first_name=form.firstname.data, last_name=form.lastname.data, email=form.email.data,
                    password_hash=generate_password_hash(form.password.data, method='sha256'), group_id=2, active=False)

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    # send the user to the login page
    return redirect(url_for('auth.login'))


@bp.route('/login/', methods=['GET'])
def login():
    form = LoginForm()
    return render_template('resources/auth/login.html', form=form)


@bp.route('/login/', methods=['POST'])
def login_post():
    form = LoginForm(request.form)

    # check if the user exists
    user = db.session.query(User).filter_by(email=form.email.data).first()

    if not form.validate():
        return render_template('resources/auth/login.html', form=form)

    # check if the user is allowed to login
    if user and user.active == False:
        flash('Ihr Account wurde noch nicht freigeschaltet. Wenden Sie sich an einen Administrator.', 'danger')
        return render_template('resources/auth/login.html', form=form)

    # if the user does not exist or the password is wrong, redirect to the login page
    if not user or not check_password_hash(user.password_hash, form.password.data):
        flash('Bitte überprüfen Sie ihre Eingaben. E-Mail und Passwort stimmen nicht überein    ', 'danger')
        return render_template('resources/auth/login.html', form=form)

    # if the user exists and the password is correct, log the user in
    login_user(user, remember=True)
    return url_for('main.index')


@bp.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
