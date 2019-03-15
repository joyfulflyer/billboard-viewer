import os
import logging
from . import flask_db
from flask import Flask
import time


def create_app(test_config=None):
    app = Flask(__name__,
                instance_path=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'instance')),
                instance_relative_config=True)
    db_path = os.path.join(app.instance_path, '..', 'charts.db')
    logging.warning(time.asctime() + " Setting database path to: " + db_path)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=db_path,
    )

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

    flask_db.init_app(app)

    from . import find_song
    app.register_blueprint(find_song.bp)

    from . import show_song
    app.register_blueprint(show_song.bp)

    from . import home
    app.register_blueprint(home.bp)

    from . import login
    app.register_blueprint(login.bp)

 #   app.add_url_rule('/', 'hello', 'this is text')

    return app
