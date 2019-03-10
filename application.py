import reader
import logging
from pathlib import Path

file_name = 'logs.log'
path = '/opt/python/logs/'

if not Path(path).exists():
    path = './'

logging.basicConfig(filename=path+file_name, filemode='w')
application = reader.create_app()


if __name__ == "__main__":
    application.debug = True
    application.run()
