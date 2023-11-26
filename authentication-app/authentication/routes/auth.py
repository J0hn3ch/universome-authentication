from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from authentication.model.form import LoginForm

bp = Blueprint('auth', __name__, url_prefix='/auth')

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"

def init_app_login_manager(app=None):
    return login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_username):
    return None

@bp.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    form = LoginForm()
    if form.validate_on_submit():
        pass

    return render_template('auth/login.html', title='Login', form=form)

@bp.route('/register', methods=('GET', 'POST'))
def register():
    return render_template('auth/register.html')
