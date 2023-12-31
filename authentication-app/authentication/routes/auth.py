from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from flask import (
    Blueprint, flash, current_app, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from authentication.model.form import LoginForm, RegistrationForm
from authentication.controller.UserController import UserController

bp = Blueprint('auth', __name__, url_prefix='/auth')

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "auth.login"
login_manager.login_message_category = "info"
#login_manager.init_app(current_app)

def init_app_login_manager(app=None):
    return login_manager.init_app(app)

@bp.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()

    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect(url_for('main.dashboard'))        
        return render_template('auth/auth.html', title='Login', form=form)

    if request.method == 'POST':
        if current_user.is_authenticated:
            return redirect(url_for('main.dashboard'))
        
        username = request.form['username']
        password = request.form['password']
        remember = True if request.form.get('remember') else False
        # Check nonce
        # Check request
        # Check Cross-origin
        # Check data
        # Request to the controller to perform elaboration of data before send it to Model
        user_controller = UserController(username, password)
        if form.validate_on_submit():
            # Hashing password
            #s = form.username.data + " " + form.password.data
            try:
                user = user_controller.login()

                if user is not None:
                    #login_user(user)
                    flash('Logged in successfully.', 'success')
                    login_user(user, remember=remember)
                    return redirect(url_for('main.dashboard'))
                    #return "Username and Password are correct! " + s
                else:
                    flash("Invalid Username or password!", "danger")
                    return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page
            except Exception as e:
                flash(e, "danger")
        
        
    
    return None

@bp.route('/register', methods=('GET', 'POST'))
def register():
    form = RegistrationForm()

    if request.method == 'GET':        
        return render_template('auth/auth.html', title='Registration', form=form)
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if form.validate_on_submit():
            # Hashing password
            s = form.username.data + " " + form.password.data
            return "Registration" + s
        
@bp.route('/signup')
def signup():
    return 'Signup'

@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@login_manager.user_loader
def load_user(user_id):
    return UserController.getUserById(int(user_id))

@login_manager.request_loader
def request_loader(request):
    pass

@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized', 401

# @login_manager.user_loader
# def user_loader(email):
    #error = None
    #user = db.execute(
    #    'SELECT * FROM user WHERE username = ?', (username,)
    #).fetchone()

    #if user is None:
    #    error = 'Incorrect username.'
    #elif not check_password_hash(user['password'], password):
    #    error = 'Incorrect password.'
    
    #if error is None:
    #    session.clear()
    #    session['user_id'] = user['id']
    #    return redirect(url_for('index'))
    
    #flash(error)

    # if email not in users:
    #     return

    # user = User()
    # user.username = email
    # return user