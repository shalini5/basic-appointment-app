# services/notable/project/__init__.py

import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# instantiate the db
db = SQLAlchemy()


def create_app(script_info=None):

    # instantiate the app
    app = Flask(__name__)

    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # set up extensions
    db.init_app(app)

    # register blueprints
    from project.api.appointments import appt_blueprint
    from project.api.doctors import doctors_blueprint
    app.register_blueprint(appt_blueprint)
    app.register_blueprint(doctors_blueprint)

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}

    return app