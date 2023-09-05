from decouple import config
import logging

SERVER_ADDRESS = config("server.address", default="0.0.0.0")
SERVER_PORT = config("server.port", default=5000)

logging.info("Reading configurations....")
logging.info("==============================================================")
logging.info("SERVER_ADDRESS = " + SERVER_ADDRESS)
logging.info("SERVER_PORT = " + SERVER_PORT)
logging.info("==============================================================")
