from flask import Flask, render_template
from flask_login import LoginManager
#from flask_bcrypt import Bcrypt

import os

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'universome.sqlite'),
        SQLALCHEMY_DATABASE_URI="sqlite:///database.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=True
    )
    app.debug = True
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

    #from .routes import members
    #app.register_blueprint(members.mbr)

    #from . import login
    #login.init_app_login_manager(app) 

    #from . import routes
    #app.register_blueprint(routes.lgn)
    #from . import auth
    #app.register_blueprint(auth.bp)
    
    return app