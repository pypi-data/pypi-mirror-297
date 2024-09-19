import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
import os

logger = logging.getLogger('logit')


def setup_logging(log_level, enable_logging):

    if not enable_logging:
        logger.disabled = True
        return

    now = datetime.now().strftime('%Y-%m-%d')
    log_filename = os.path.join(os.getcwd(), f'app_log_{now}.log')

    handler = RotatingFileHandler(log_filename)
    handler.setLevel(log_level)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger.setLevel(log_level)
    logger.addHandler(handler)

    logger.propagate = False


