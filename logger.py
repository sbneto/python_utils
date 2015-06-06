__author__ = 'Samuel'

import functools
import logging
import inspect


def initialize_logging(name, file_name=None):
    if file_name:
        logging.basicConfig(filename=file_name, format='%(asctime)s %(levelname)s: (%(name)s) %(message)s')
    else:
        logging.basicConfig(format='%(asctime)s %(levelname)s: (%(name)s) %(message)s')
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
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
            try:
                frame = inspect.stack()[1]
                module = inspect.getmodule(frame[0])
                logger.debug('(%s) Entering function %s' % (module.__name__, f.__name__))
                result = f(*args, **kwargs)
                logger.debug('(%s) Exiting function %s' % (module.__name__, f.__name__))
                return result
            except Exception as e:
                logger.exception(e)
                raise e
            finally:
                del module
                del frame
        return wrapper
    return wrapper_with_args