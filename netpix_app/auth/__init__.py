from flask import Flask
from netpix_app.config import DevelopmentConfig
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    '''
    Initialise the Netpix Flask application.
    :type config_classname: Specifies the configuration class
    :rtype: Returns a configured Flask object
    '''

    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    db.init_app(app)

    return app