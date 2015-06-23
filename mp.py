__author__ = 'Samuel'

import os
import multiprocessing as _mp

from threading import Lock
from multiprocessing.managers import BaseManager
from multiprocessing.connection import wait

from .logger import initialize_logging

log = initialize_logging()


def add_process(processes, func, arg):
    p = _mp.Process(target=func, args=arg)
    p.start()
    processes[p.sentinel] = p


class Pool:
    def __init__(self, processes=None):
        self.processes = processes if processes else os.cpu_count() + 2

    def map(self, func, iterable, chunksize=None):
        args = iter(iterable)
        existing_processes = {}

        arg = next(args, False)
        while len(existing_processes) < self.processes and arg:
            add_process(existing_processes, func, arg)
            arg = next(args, False)

        while existing_processes:
            for s in wait(existing_processes):
                del existing_processes[s]
                if arg:
                    add_process(existing_processes, func, arg)
                    arg = next(args, False)

class ResourceLock:
    def __init__(self):
        self.locks = {}

    def acquire(self, resource, blocking=True, timeout=-1):
        try:
            self.locks[resource].acquire(blocking, timeout)
        except KeyError:
            self.locks[resource] = Lock()
            self.locks[resource].acquire(blocking, timeout)

    def release(self, resource):
        self.locks[resource].release()

class ResourceManager(BaseManager):
    pass

ResourceManager.register('ResourceLock', ResourceLock)
