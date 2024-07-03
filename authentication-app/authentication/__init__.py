from flask import Flask
from flask_cors import CORS
from authentication.controller.CoapController import entranceObserverClient
#from flask_bcrypt import Bcrypt
import os
from serial import Serial

# [Import - Styling]: Sass compile in development
from flask_assets import Environment, Bundle
from sassutils.wsgi import SassMiddleware
import asyncio
from aiocoap import *

#global DATABASE
#DATABASE = os.path.join(app.instance_path, 'universome.sqlite')
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, static_folder='static', template_folder="templates", instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='universome',
        DATABASE=os.path.join(app.instance_path, 'universome.sqlite'),
        SQLALCHEMY_DATABASE_URI="sqlite:///database.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=True
    )
    app.debug = True
    app.app_context().push()
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Styling: Sass compile
    '''
    app.wsgi_app = SassMiddleware(app.wsgi_app, {'authentication': ('static/sass', 'static/css', '/static/css', True )})
    assets = Environment(app)
    css = Bundle('sass/main.scss',
             filters=['libsass'],
             output='css/style.scss.css',
             depends='scss/*.scss')
    assets.register("asset_css", css)
    css.build(disable_cache=True)
    '''
    
    #bcrypt = Bcrypt(app)

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

    # Main Blueprint
    from .routes.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Authentication Blueprint
    from .routes import auth
    auth.init_app_login_manager(app)
    app.register_blueprint(auth.bp)

    # APIs
    from .api.routes import api as api_blueprint
    app.register_blueprint(api_blueprint)

    # CoAP APIs
    from .api.routes_coap import coap_api as api_coap_blueprint
    app.register_blueprint(api_coap_blueprint)
    
    # Member View
    from .routes import member
    app.register_blueprint(member.mbr)

    #from . import auth
    #app.register_blueprint(auth.bp)
    # @app.after_request
    # def after_request(response):
    #     asyncio.run(entranceObserverClient())
    return app