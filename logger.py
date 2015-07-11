__author__ = 'Samuel'

import functools
import logging
import inspect


def initialize_logging(name=None, file_name=None):
    if not name:
        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0])
        logger_name = module.__name__
        del module
        del frame
    log_format = '%(asctime)s %(levelname)s: (%(name)s) %(message)s'
    if file_name:
        logging.basicConfig(filename=file_name, format=log_format)
    else:
        logging.basicConfig(format=log_format)
    logger = logging.getLogger(name if name else logger_name)
    logger.setLevel(logging.INFO)
    return logger


def basic_log(logger=None):
    def wrapper_with_args(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except Exception as e:
                logger.exception(e)
                raise e
        return wrapper
    return wrapper_with_args


def trace_log(logger=None):
    def wrapper_with_args(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            logger.debug('Entering function %s' % f.__name__)
            result = f(*args, **kwargs)
            logger.debug('Exiting function %s' % f.__name__)
            return result
        return wrapper
    return wrapper_with_args