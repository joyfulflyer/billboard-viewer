import reader
import logging
import sys
from pathlib import Path
import config

file_name = 'logs.log'
path = '/opt/python/logs/'

if not Path(path).exists():
    path = './'


file_handler = logging.FileHandler(filename=path+file_name)
file_handler.setLevel(logging.DEBUG)
std_out_handler = logging.StreamHandler(sys.stdout)
std_out_handler.setLevel(logging.NOTSET)
handlers = [file_handler, std_out_handler]

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)

logging.basicConfig(handlers=handlers)

application = reader.create_app(config.TestConfig)


if __name__ == "__main__":
    application.debug = True
    application.run()
