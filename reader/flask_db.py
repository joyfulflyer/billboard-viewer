import sqlite3

from flask import current_app, g
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy


def get_db():
    if 'db' not in g:
        g.db = SQLAlchemy(current_app)
#        g.db = sqlite3.connect(current_app.config['DATABASE'])
#        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None and db.session is not None:
        db.session.close()


def init_app(app):
    app.teardown_appcontext(close_db)
