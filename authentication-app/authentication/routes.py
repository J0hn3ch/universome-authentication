from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, abort
)
from flask_login import login_user, login_required, logout_user
from .view.form.form import LoginForm, RegistrationForm

from .db import get_db
from .login import User

lgn = Blueprint('auth', __name__, url_prefix='/auth')

@lgn.route('/register', methods=('GET', 'POST'))
def register():

    form = RegistrationForm()
    if request.method == 'GET':
        return render_template('auth/register.html', form=form)
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')

@lgn.route('/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    if request.method == 'GET':
        return render_template('auth/login.html', form=form)
    
    elif request.method == 'POST':
        if form.validate_on_submit():
            # Login and validate the user.
            # user should be an instance of your `User` class
            user = User(form.username.data)
            login_user(user)

            flash('Logged in successfully.')

            next = request.args.get('next')
            # url_has_allowed_host_and_scheme should check if the url is safe
            # for redirects, meaning it matches the request host.
            # See Django's url_has_allowed_host_and_scheme for an example.
            if not url_has_allowed_host_and_scheme(next, request.host):
                return abort(400)

            return redirect(next or url_for('index'))

@lgn.route("/settings")
@login_required
def settings():
    pass

@lgn.route('/logout')
def logout():
    logout_user()
    return 'Logged out'