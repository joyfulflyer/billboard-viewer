import reader
import logging
import sys
from pathlib import Path
import config

file_name = 'logs.log'
path = '/opt/python/logs/'

if not Path(path).exists():
    path = './'

application = reader.create_app(config.TestConfig)

if __name__ == "__main__":
    application.debug = True
    application.run(host="0.0.0.0")
