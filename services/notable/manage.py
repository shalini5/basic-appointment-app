# services/notable/manage.py

import sys
import pytest

from flask.cli import FlaskGroup

from project import create_app, db
from project.api.models import Doctor, Appointment

app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command('recreate_db')
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command()
def test():
    """Runs the tests without code coverage"""
    options = '--cov=project/tests'

    pytest.main([options])
    sys.exit(0)


@cli.command('seed_db')
def seed_db():
    """Seeds the database."""
    db.session.add(Doctor(name='adam', email="adam@gmail.com"))
    db.session.add(Doctor(name='alice', email="alice@gmail.com"))
    db.session.add(Doctor(name='bob', email="bob@gmail.com"))
    db.session.add(Doctor(name='charlie', email="charlie@gmail.com"))
    db.session.commit()


if __name__ == '__main__':
    cli()
