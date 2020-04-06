import logging
import logging.config
import sys
from logging import FileHandler
from logging.handlers import RotatingFileHandler
import os

from common.constants import g_PYTHON_START, g_DEBUG
from common.path import LOG_FOLDER

ROOT_LOG = 'common.log'
OUTPUT_LOG = 'only_gui.log'

if g_PYTHON_START:
    # в случае запуска из pyCharm использовать root папку для логов
    LOG_FOLDER = os.path.join(os.getcwd(), 'Logs')

if not os.path.exists(LOG_FOLDER) and not g_DEBUG:
    os.makedirs(LOG_FOLDER, mode=777)

DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
ROOT_FORMATTER = logging.Formatter(
    fmt="%(asctime)s > %(filename)s > %(lineno)s > %(levelname)s : %(message)s",
    datefmt=DATE_FORMAT
)

CONSOLE_FORMATTER = logging.Formatter(
    fmt="%(asctime)s > %(filename)s > %(lineno)s > %(levelname)s : %(message)s",
    datefmt=DATE_FORMAT
)

LOGGER_FORMATTER = logging.Formatter(
    fmt="%(asctime)s > %(module)s > %(levelname)s : %(message)s",
    datefmt=DATE_FORMAT
)


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(CONSOLE_FORMATTER)
    console_handler.setLevel(logging.DEBUG)
    return console_handler


def get_file_handler():
    file_handler = RotatingFileHandler(os.path.join(LOG_FOLDER, ROOT_LOG), maxBytes=4096, encoding='utf-8')
    file_handler.setFormatter(ROOT_FORMATTER)
    file_handler.setLevel(logging.DEBUG)
    return file_handler


def get_current_launch_file_handler():
    file_handler = FileHandler(os.path.join(LOG_FOLDER, OUTPUT_LOG), mode='w', encoding='utf-8')
    file_handler.setFormatter(LOGGER_FORMATTER)
    file_handler.setLevel(logging.INFO)
    return file_handler


root = logging.getLogger()
root.setLevel(logging.DEBUG)
root.addHandler(get_console_handler())
if g_DEBUG:
    root.addHandler(get_file_handler())

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
if g_DEBUG:
    logger.addHandler(get_current_launch_file_handler())
