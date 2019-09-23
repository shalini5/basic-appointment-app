# services/notable/project/config.py
import os

class BaseConfig:
    """ Base Configuration """
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'my_precious'


class DevelopmentConfig(BaseConfig):
    """ Development Config """
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class TestingConfig(BaseConfig):
    """ Testing Config """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_TEST_URL')


class ProductionConfig(BaseConfig):
    """ Production Config  """
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

