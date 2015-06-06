__author__ = 'Samuel'

import bz2

from collections import OrderedDict
from .logger import *

log = initialize_logging(__name__)


class FilePool:
    def __init__(self, size):
        self.size = size
        self.pool = OrderedDict()

    def open(self, filename, mode):
        if filename in self.pool:
            self.pool.move_to_end(filename, last=False)
            return self.pool[filename]

        f = bz2.open(filename, mode)
        if len(self.pool) >= self.size:
            _, old_f = self.pool.popitem(last=False)
            old_f.close()
        self.pool[filename] = f
        return f

    def close(self):
        for f in self.pool.values():
            f.close()
