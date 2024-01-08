from flask import Flask
#from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO, emit

import os
from serial import Serial

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='universome',
        DATABASE=os.path.join(app.instance_path, 'universome.sqlite'),
        SQLALCHEMY_DATABASE_URI="sqlite:///database.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=True
    )
    app.debug = True
    app.app_context().push()
    #bcrypt = Bcrypt(app)

    #global DATABASE
    #DATABASE = os.path.join(app.instance_path, 'universome.sqlite')

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # Database Initialization > Database population
    from . import db
    db.init_app(app)

    # APIs
    #from .api import

    # Main Blueprint
    from .routes.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Authentication Blueprint
    from .routes import auth
    auth.init_app_login_manager(app)
    app.register_blueprint(auth.bp)

    socketio = SocketIO(app, cors_allowed_origins='*')
    """
    Decorator for connect
    """
    @socketio.on('connect')
    def connect():
        global thread
        print('Client connected')

        global thread
        with thread_lock:
            if thread is None:
                thread = socketio.start_background_task(background_thread)

    """
    Decorator for disconnect
    """
    @socketio.on('disconnect')
    def disconnect():
        print('Client disconnected',  request.sid)

    #from .routes import members
    #app.register_blueprint(members.mbr)

    #from . import routes
    #app.register_blueprint(routes.lgn)
    #from . import auth
    #app.register_blueprint(auth.bp)
    
    return app