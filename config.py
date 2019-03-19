from os import environ

username = "read_billboard" # environ['USERNAME']
password = "#23Kpq$M4Tnwd%PJMve"
host = environ.get('HOST')
db_name = environ.get('DATABASE')
secret_key='u9DCvDN82*$^!xbH#UG'
SQLALCHEMY_TRACK_MODIFICATIONS=False


def create_url_from_parts(username, password, host, dbname):
    password = urllib.parse.quote_plus(password)
    url = "mysql+pymysql://%s:%s@%s/%s" % (username, password, host, dbname)
    logger.error(url)
    return url
