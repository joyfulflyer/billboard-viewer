import os
import logging
from . import flask_db
from flask import Flask
import time

logger = logging.getLogger(__name__)


def create_app(test_config=None):
    app = Flask(__name__,
                instance_path=os.path.abspath(
                    os.path.join(os.path.dirname(__file__), '..', 'instance')),
                instance_relative_config=True)
    # SQLite
    db_path = os.path.join(app.instance_path, '..', 'charts.db')
    sql_alchemy_sqlite_url = "sqlite:///{}".format(db_path)
    logger.info(time.asctime() + " SQLite database path: " + db_path)

    app.config.from_mapping(
        SECRET_KEY='u9DCvDN82*$^!xbH#UG',
        SQLALCHEMY_DATABASE_URI=sql_alchemy_sqlite_url,
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_object(config.Config)
    else:
        # load the test config if passed in
        app.config.from_object(test_config)

    flask_db.init_app(app)

    #    from . import find_song
    #    app.register_blueprint(find_song.bp)

    #    from . import show_song
    #    app.register_blueprint(show_song.bp)

    #    from . import home
    #    app.register_blueprint(home.bp)

    #    from . import find_artist
    #    app.register_blueprint(find_artist.bp)

    from . import json_api
    app.register_blueprint(json_api.bp)

    #   app.add_url_rule('/', 'hello', 'this is text')

    return app
