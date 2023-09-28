import os
import sys

from loguru import logger as loguru_logger

from src.constants.path import LOG_FOLDER

if not os.path.exists(LOG_FOLDER):
    os.makedirs(LOG_FOLDER)

loguru_logger.remove()

if os.environ.get("DEBUG"):
    loguru_logger.add(sys.stdout, level="DEBUG", diagnose=False, backtrace=False)
else:
    log_file = os.path.join(LOG_FOLDER, "{time:YYYY-MM-DD}.log")
    loguru_logger.add(
        log_file,
        level="DEBUG",
        rotation="1 day",
        retention="7 days",
        compression="zip",
        diagnose=False,
        backtrace=False,
    )

    custom_format = (
        "<green>{time:HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{extra[name]: <8}</cyan> | <level>{message}</level>"
    )
    loguru_logger.add(sys.stdout, level="INFO", format=custom_format, colorize=True)

app_logger = loguru_logger.bind
