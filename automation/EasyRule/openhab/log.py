import logging
import functools
import traceback

from org.slf4j import Logger, LoggerFactory

LOG_PREFIX = "org.eclipse.smarthome.automation.rules"

def log_traceback(fn):
    """Decorator to provide better Jython stack traces"""
    functools.wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as ex:
            tb = traceback.format_exc().splitlines()

            if len(args) > 0 and hasattr(args[0], "log"):
                for line in tb:
                    args[0].log.error(line)
            else:
                for line in tb:
                    print(line)
                    default_logger.error(line)
    return wrapper

class Slf4jHandler(logging.Handler):
    def emit(self, record):
        message = self.format(record)
        logger_name = record.name
        if record.name == "root":
            logger_name = Logger.ROOT_LOGGER_NAME
        logger = LoggerFactory.getLogger(logger_name)
        level = record.levelno
        if level == logging.DEBUG:
            logger.debug(message)
        elif level == logging.INFO:
            logger.info(message)
        elif level == logging.WARN:
            logger.warn(message)
        elif level in [logging.ERROR, logging.CRITICAL] :
            logger.error(message)
            
handler = Slf4jHandler()
logging.root.setLevel(logging.DEBUG)
logging.root.handlers = [handler]

default_logger = logging.getLogger(LOG_PREFIX)