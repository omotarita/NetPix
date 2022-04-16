from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_required
from flask.helpers import get_root_path
from pathlib import Path
import dash
from dash import Dash
import dash_bootstrap_components as dbc
#import pandas as pd


csrf = CSRFProtect()
db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_class_name):
    '''
    Initialise the Netpix Flask application.
    :type config_classname: Specifies the configuration class
    :rtype: Returns a configured Flask object
    '''

    app = Flask(__name__)
    app.config.from_object(config_class_name) 
    csrf.init_app(app)
    csrf._exempt_views.add('dash.dash.dispatch')
    db.init_app(app)
    #login_manager.init_app(app)
    #csrf.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    register_dashapp(app)

    with app.app_context():
        from netpix_app.models import User
        db.create_all()

    #with app.app_context():
        # Import Dash app
        # from dash_app.dash import init_dashboard
        # app = init_dashboard(app)

    from netpix_app.auth.routes import auth_bp
    app.register_blueprint(auth_bp)

    return app

def register_dashapp(app):
    from netpix_app.dashboard import layout
    from netpix_app.dashboard.callbacks import register_callbacks

    meta_viewport = {"name": "viewport", "content": "width=device-width, initial-scale=1, shrink-to-fit=no"}
    external_stylesheets = [Path(__file__).parent.parent.parent.joinpath('netpix_app/static/assets/css', 'custom.css')]

    dashapp = dash.Dash(__name__,
                         server=app,
                         url_base_pathname='/dashboard/',
                         assets_folder=get_root_path(__name__) + '/dashboard/assets/',
                         meta_tags=[meta_viewport],
                         external_stylesheets = ['assets/custom.css', dbc.themes.BOOTSTRAP]
                         )

    with app.app_context():
        dashapp.title = 'Dashboard'
        dashapp.layout = layout.layout
        register_callbacks(dashapp)

    _protect_dash_views(dashapp)


def _protect_dash_views(dash_app):
    for view_func in dash_app.server.view_functions:
        if view_func.startswith(dash_app.config.routes_pathname_prefix):
            dash_app.server.view_functions[view_func] = login_required(dash_app.server.view_functions[view_func])