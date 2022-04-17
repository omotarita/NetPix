
import secrets
from pathlib import Path
from flask_sqlalchemy import SQLAlchemy


#print(secrets.token_urlsafe(16))

class Config(object):
    """
    Sets the global basic Flask configuration that is shared across all environments
    """
    DEBUG = False # Turns on debugging features in Flask
    SECRET_KEY = 'NS18dOS2VXubcs4e9z17CQ'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOADED_PHOTOS_DEST = Path(__file__).parent.joinpath("static/assets/images")
    ## DATA_PATH = Path('data') - keep commented
    #database_file = Path(__file__).parent.parent.joinpath("data", "example.sqlite")
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(database_file)

class ProductionConfig(Config):
    ENV = 'production'

class DevelopmentConfig(Config):
    ENV = 'development'
    DEBUG = True
    database_file = Path(__file__).parent.parent.joinpath("data", "example.sqlite")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(database_file)
    SQLALCHEMY_ECHO = True

class TestingConfig(Config):
    ENV = 'testing'
    TESTING = True
    SQLALCHEMY_ECHO = True