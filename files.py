__author__ = 'Samuel'

import bz2
import builtins
import zipfile
import scandir
import os
import shutil

from collections import OrderedDict

from .logger import initialize_logging
from .utils import path_name

log = initialize_logging()


def zip(input_path, output_path=None, compression=None, keep_input=False, keep_root=False):
    tmp_path = False
    if not output_path:
        if keep_input:
            output_path = '%s.zip' % input_path
        else:
            output_path = '%s.tmp' % input_path
            tmp_path = True

    base_path = os.path.dirname(input_path) if keep_root else input_path
    with open(output_path,
              'w',
              file_type='zip',
              compression=compression) as zip_f:
        for curr_dir, dir_list, files_list in scandir.walk(input_path):
            virtual_dir = curr_dir.replace(base_path, '')
            for file_name in files_list + dir_list:
                file_path = path_name(curr_dir, file_name)
                virtual_path = path_name(virtual_dir, file_name)
                zip_f.write(file_path, virtual_path)

    if not keep_input:
        shutil.rmtree(input_path, ignore_errors=True)
    if tmp_path:
        os.rename(output_path, output_path[:-4])


def open(filename, mode, encoding=None, file_type=None, compression=None):
    if not encoding and 't' in mode:
        encoding = 'utf-8'

    if compression == 'bz2':
        compression = zipfile.ZIP_BZIP2
    else:
        compression = zipfile.ZIP_STORED

    if file_type == 'bz2':
        f = bz2.open(filename, mode, encoding=encoding)
    elif file_type == 'zip':
        f = zipfile.ZipFile(filename, mode, compression, True)
    else:
        f = builtins.open(filename, mode, encoding=encoding)
    return f


class FilePool:
    def __init__(self, size, compression=None):
        self.size = size
        self.compression = compression
        self.pool = OrderedDict()
        self.hit = 0
        self.miss = 0

    def open(self, filename, mode, encoding=None, file_type=None, compression=None):
        if filename in self.pool:
            self.pool.move_to_end(filename, last=False)
            self.hit += 1
            return self.pool[filename]

        f = open(filename, mode, encoding, file_type, compression)

        if len(self.pool) >= self.size:
            _, old_f = self.pool.popitem(last=False)
            old_f.close()
        self.pool[filename] = f
        
        self.miss += 1
        return f

    def close(self):
        for f in self.pool.values():
            f.close()
