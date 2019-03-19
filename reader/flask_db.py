import sqlite3
from flask import current_app, g
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
import logging


logger = logging.getLogger(__name__)
db = SQLAlchemy()


def get_db():
    if 'db' not in g:
        g.db = db.session
#        g.db = sqlite3.connect(current_app.config['DATABASE'])
#        g.db.row_factory = sqlite3.Row

    return g.db


def init_app(app):
    db.init_app(app)
