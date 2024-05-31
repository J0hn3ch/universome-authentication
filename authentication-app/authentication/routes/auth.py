from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from flask import (
    Blueprint, flash, current_app, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from authentication.model.form import LoginForm, RegistrationForm
from authentication.controller.UserController import UserController

bp = Blueprint('auth', __name__, url_prefix='/auth')

login_manager = LoginManager()
login_manager.init_app(current_app)
login_manager.session_protection = "strong"
login_manager.login_view = "auth.login"
login_manager.login_message_category = "info"

def init_app_login_manager(app=None):
    return login_manager.init_app(app)

@bp.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()

    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect(url_for('main.dashboard'))        
        return render_template('auth/auth.html', title='Login', form=form)

    elif request.method == 'POST':
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

                    flash('Logged in successfully.', 'success')
                    login_user(user, remember=remember)
                    return redirect(url_for('main.dashboard'))
                else:
                    flash("Invalid Username or password!", "danger")
                    return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page
                
                #next = request.args.get('next')
                #if not url_has_allowed_host_and_scheme(next, request.host):
                #    return abort(400)
                #return redirect(next or url_for('index'))
            except Exception as e:
                flash(e, "danger")
        
        
    
    return None

@bp.route('/register', methods=('GET', 'POST'))
def register():
    form = RegistrationForm()

    if request.method == 'GET':        
        return render_template('auth/auth.html', title='Registration', form=form)
    
    elif request.method == 'POST':
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
            """
            if error is None:
                try:
                    #db.execute("INSERT INTO user (username, password) VALUES (?, ?)",(username, generate_password_hash(password)),)
                    #db.commit()
                    pass
                except db.IntegrityError:
                    error = f"User {username} is already registered."
                else:
                    return redirect(url_for("auth.login"))
            else:
                flash(error)
            """
            return render_template('auth/register.html')
        
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