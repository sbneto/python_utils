__author__ = 'Samuel'

import os
import multiprocessing as _mp
import itertools

from threading import Lock
from multiprocessing.managers import BaseManager
from multiprocessing.connection import wait

from .logger import initialize_logging

log = initialize_logging()


def add_process(processes, func, arg):
    p = _mp.Process(target=func, args=arg, name=str(len(processes)))
    p.start()
    processes[p.sentinel] = p


def loop_function(f, args):
    for arg in args:
        try:
            f(*arg)
        except Exception as e:
            log.exception(e)


def get_arg(args, chuncksize):
    if chuncksize:
        return [u for u in itertools.islice(args, 0, chuncksize)]
    else:
        return [u for u in itertools.islice(args, 0, 1)]


class Pool:
    def __init__(self, processes=None):
        self.processes = processes if processes else os.cpu_count() + 2

    def map(self, func, iterable, chunksize=None):
        args = iter(iterable)
        existing_processes = {}

        arg = get_arg(args, chunksize)
        while len(existing_processes) < self.processes and arg:
            add_process(existing_processes, loop_function, (func, arg))
            arg = get_arg(args, chunksize)

        while existing_processes:
            failed = set()
            for s in wait(existing_processes):
                if existing_processes[s].exitcode is not None:
                    if s in failed:
                        log.error('%s: Process sentinel is ready and exitcode is now available as %s' %
                                  (s, existing_processes[s].exitcode))
                    if existing_processes[s].exitcode != 0:
                        raise ChildProcessError('Exit code %s' % existing_processes[s].exitcode)
                    del existing_processes[s]
                    if arg:
                        add_process(existing_processes, loop_function, (func, arg))
                        arg = get_arg(args, chunksize)
                else:
                    if s not in failed:
                        log.error('%s: Process sentinel is ready but exitcode is %s' %
                                  (s, existing_processes[s].exitcode))
                        failed.add(s)


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
