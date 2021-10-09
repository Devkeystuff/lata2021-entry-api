import logging
import sys
import os
import traceback
from datetime import datetime

class LoggingUtils:
  def __init__(self, filename=None, prefix='auto') -> None:
      LoggingUtils.init(filename)

  @staticmethod
  def init(filename=None, prefix='auto'):
    logger = logging.getLogger()

    filename = os.path.abspath('./logs/' + datetime.now().strftime(f'{prefix}_%y_%m_%d') + '.log')

    file_logger = logging.FileHandler(filename)
    logger.addHandler(file_logger)

    console_logger = logging.StreamHandler()
    logger.addHandler(console_logger)

  @staticmethod
  def error(message):
    logging.error(message) 

  @staticmethod
  def log_exception(e: Exception):
    LoggingUtils.error(str(e))
    exc_type, exc_value, exc_tb = sys.exc_info()
    LoggingUtils.error("\n".join(traceback.format_exception(exc_type, exc_value, exc_tb)))