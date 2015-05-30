__author__ = 'Samuel'

import os
import json
import functools
import utils

from utils.list_folder import list_folder


def is_current_version(results_id, data_path, args):
    try:
        version_path = '%s\\%s\\version.json' % (data_path, results_id)
        if os.path.isfile(version_path):
            with open(version_path, 'r') as f:
                version_file = json.load(f)
            if version_file['status'] == 'success' and argseq(args, version_file['args']):
                return True
    except ValueError:
        pass
    return False


def write_version(results_id, data_path, status, args):
    version_path = '%s\\%s\\version.json' % (data_path, results_id)
    files_path = '%s\\%s\\files' % (data_path, results_id)
    os.makedirs(files_path, exist_ok=True)
    version_file = {'args': args, 'status': status}
    with open(version_path, 'w') as f:
        json.dump(version_file, f)


def write_result_set(results_id, data_path, sets_path):
    set_file = '%s\\%s.json' % (sets_path, results_id)
    files_path = '%s\\%s\\files' % (data_path, results_id)
    files_list = list_folder(files_path, full_path=True)
    with open(set_file, 'w') as f:
        json.dump(files_list, f)


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


def file_cache(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        if not is_current_version(args[0], args[1], args):
            write_version(args[0], args[1], 'running', args)
            result = f(*args, **kwargs)
            write_version(args[0], args[1], 'success', args)
            write_result_set(args[0], args[1], args[2])
            return result
        return False
    return wrapper
