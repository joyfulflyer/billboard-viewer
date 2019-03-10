import reader
import logging

logging.basicConfig(filename='/opt/python/log/logs.log', filemode='a')
application = reader.create_app()

logging.error("find")

if __name__ == "__main__":
    application.debug = True
    application.run()
