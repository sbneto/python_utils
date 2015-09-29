__author__ = 'Samuel'

import os
import json
import functools
import time

from inspect import signature

from .logger import initialize_logging

log = initialize_logging()


def get_path(id_):
    return './.file_cache/%s_version.json' % (id_.replace('C:/', '')
                                              .replace('c:/', '')
                                              .replace('C:\\', '')
                                              .replace('c:\\', '')
                                              .replace('/', '_'))


def get_version(id_):
    os.makedirs('./.file_cache', exist_ok=True)
    version_path = get_path(id_)
    try:
        with open(version_path, 'r') as f:
            version_file = json.load(f)
        return version_file
    except FileNotFoundError:
        return {}


def write_version(id_, status, args):
    os.makedirs('./.file_cache', exist_ok=True)
    version_path = get_path(id_)
    version_data = {'status': status, 'timestamp': time.time(), 'args': args}
    with open(version_path, 'w') as f:
        json.dump(version_data, f)


def dicteq(d1, d2):
    if len(d1) != len(d2):
        return False
    for key, value in d1.items():
        if key not in d2:
            return False
        if value != d2[key]:
            return False
    return True


def argseq(arg1, arg2):
    if len(arg1) != len(arg2):
        return False
    for e1, e2 in zip(arg1, arg2):
        if type(e1) == type(e2) == dict:
            if not dicteq(e1, e2):
                return False
        elif e1 != e2:
            return False
    return True


def is_version(version, verify):
    try:
        if type(verify) is tuple:
            return argseq(verify, version['args'])
        else:
            return version['status'] == verify
    except (ValueError, KeyError):
        return False


def file_cache(path_name=None):
    def wrapper_with_args(f):
        arg_pos = list(signature(f).parameters).index(path_name)

        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            id_ = args[arg_pos]
            current = get_version(id_)
            if not is_version(current, args) or not is_version(current, 'success'):
                write_version(id_, 'running', args)
                try:
                    result = f(*args, **kwargs)
                except Exception:
                    raise
                write_version(id_, 'success', args)
                return result
            return False
        return wrapper
    return wrapper_with_args
