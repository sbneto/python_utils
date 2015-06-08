__author__ = 'Samuel'

import configparser
import datetime
import pickle
from itertools import tee
import threading
import json
import ujson
import bz2

from .logger import *

log = initialize_logging(__name__)


def cross(o, a, b):
    """
    2D cross product of OA and OB vectors, i.e. z-component of their 3D cross product.
    Returns a positive value, if OAB makes a counter-clockwise turn,
    negative for clockwise turn, and zero if the points are collinear.
    """
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def check_colinear(v):
    for t in tripletwise(v):
        if cross(*t) != 0:
            return False
    return True


def pairwise(iterable):
    """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
    a, b = tee(iterable)
    next(b)
    return zip(a, b)


def grouped(iterable, n=2):
    return zip(*[iter(iterable)]*n)


def tripletwise(iterable):
    """s -> (s0,s1,s2), (s1,s2,s3), (s2,s3,s4), ..."""
    a, b, c = tee(iterable, 3)
    next(b)
    next(c)
    next(c)
    return zip(a, b, c)


def load_object(file_name):
    """
    Carrega um objeto persistido.
    :param file_name:
    """
    with open(file_name, 'rb') as fin:
        return pickle.load(fin)


def write_object(obj, file_name):
    """
    Persiste um objeto em um arquivo.
    :param obj:
    :param file_name:
    """
    with open(file_name, 'wb') as fout:
        pickle.dump(obj, fout, pickle.HIGHEST_PROTOCOL)


def load_config(file_name):
    conf = configparser.ConfigParser()
    conf.read(file_name)
    return conf


def parse_datetime(time_str):
    return datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')


def parse_date(time_str):
    return datetime.datetime.strptime(time_str, '%Y-%m-%d').date()


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)


class SafeThreadError(Exception):
    def __init__(self, message):
        self.message = message


def safe_thread_start(function, arguments, timeout):
    got_lock = threading.Event()
    thread = threading.Thread(target=function, args=(got_lock,) + arguments)
    thread.start()
    if got_lock.wait(timeout):
        return thread
    else:
        log.error('Unresponsive thread.')
        raise SafeThreadError('Unresponsive thread.')


def chooser(key):
    def element_chooser(indexable):
        return indexable[key]
    return element_chooser


def json_loader(path):
    def loader(files_dict):
        try:
            json_dict = {}
            for key, file_name in files_dict.items():
                with open('%s/%s' % (path, file_name)) as f:
                    json_dict[key] = json.load(f)
            return json_dict
        except Exception as e:
            log.exception(e)
            raise e
    return loader

def bz2_json_iterator(path):
    file_type = path.split('.')[-1]
    if file_type == 'bz2':
        with bz2.BZ2File(path, 'rb') as f:
            for line in f:
                yield ujson.loads(line.decode('utf-8'))
    else:
        with open(path, 'rt', encoding='utf-8') as f:
            for line in f:
                yield ujson.loads(line)


def write_json_object(obj, path, file_name):
    file_path = '%s/%s' % (path, file_name)
    with open(file_path, 'w') as f:
        json.dump(obj, f)


def path_name(*args):
    return '/'.join(args)
