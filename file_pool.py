__author__ = 'Samuel'

import bz2

from collections import OrderedDict

from .logger import *

log = initialize_logging()

class FilePool:
    def __init__(self, size, compression=None):
        self.size = size
        self.compression = compression
        self.pool = OrderedDict()
        self.hit = 0
        self.miss = 0

    def open(self, filename, mode, encoding=None):
        if filename in self.pool:
            self.pool.move_to_end(filename, last=False)
            self.hit += 1
            return self.pool[filename]

        if 't' in mode:
            encoding = 'utf-8'
        if self.compression == 'bz2':
            f = bz2.open(filename, mode, encoding=encoding)
        else:
            f = open(filename, mode, encoding=encoding)

        if len(self.pool) >= self.size:
            _, old_f = self.pool.popitem(last=False)
            old_f.close()
        self.pool[filename] = f
        
        self.miss += 1
        return f

    def close(self):
        for f in self.pool.values():
            f.close()
