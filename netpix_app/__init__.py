from flask import Flask
from netpix_app.config import DevelopmentConfig
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()
db = SQLAlchemy()

def create_app():
    '''
    Initialise the Netpix Flask application.
    :type config_classname: Specifies the configuration class
    :rtype: Returns a configured Flask object
    '''

    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig) #change config once developed (? - check submission advice from Week 6)
    csrf.init_app(app) #should i have both?
    db.init_app(app) #see above
    #login_manager.init_app(app)
    #csrf.init_app(app)
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