import logging
import os

from dotenv import load_dotenv


def configure_logging():
    load_dotenv()

    LOGLEVEL = logging.getLevelName(os.getenv('LOGLEVEL'))
    log_format = '%(asctime)s %(levelname)s: %(message)s'
    log_time_format = '%d.%m.%Y %H:%M:%S %z'
    logging.basicConfig(level=LOGLEVEL, format=log_format, datefmt=log_time_format)


def log_cmd(user, command):
    message = f"{user} {command}"
    logging.debug(message)
