import reader
import logging

logging.basicConfig(filename='/opt/python/log/logs.log', filemode='w')
application = reader.create_app()

if __name__ == "__main__":
    application.debug = True
    application.run()
