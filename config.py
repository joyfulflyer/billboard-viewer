from os import environ, path, getenv
import urllib.parse
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_db_type_from_variable():
    type = "sqlite:///"
    if 'DB_TYPE' in environ and "mysql" in environ['DB_TYPE']:
        type = "mysql+pymysql://"
    return type


def create_url_from_parts(username, password, host, dbname, db_file):
    url = ""
    base = get_db_type_from_variable()
    if "sqlite" in base:
        if db_file == None:
            db_file = 'charts.db'
        if not db_file.startswith('/'):
            db_file = path.abspath(path.join(path.dirname(__file__), db_file))
        url = base + db_file
    elif "mysql" in base:
        password = urllib.parse.quote_plus(password)
        url = "%s%s:%s@%s/%s" % (base, username, password, host, dbname)
    print("DB url: %r" % (url, ))
    return url


class Config:
    username = environ['DB_USERNAME']
    password = environ['PASS']
    host = environ.get('DB_HOST')
    db_name = environ.get('DATABASE')
    db_file = environ.get('DB_FILE_NAME')
    SECRET_KEY = 'u9DCvDN82*$^!xbH#UG'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = create_url_from_parts(username, password, host,
                                                    db_name, db_file)
    SEARCH_HOST = getenv('SEARCH_HOST', "localhost")


class TestConfig(Config):
    ENV = "development"
