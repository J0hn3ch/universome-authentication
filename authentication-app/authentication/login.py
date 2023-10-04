import flask_login

login_manager = flask_login.LoginManager()

class User(flask_login.UserMixin):
    def __init__(self, username, active=True):
        self.username = username
        self.active = active

users = {}

@login_manager.user_loader
def user_loader(email):
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

    if email not in users:
        return

    user = User()
    user.username = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email
    return user

@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized', 401

def init_app_login_manager(app=None):
    return login_manager.init_app(app)