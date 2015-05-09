#!/usr/bin/env python

"""
Cross-platform file lock context
"""

import os
import time
import functools
import numbers
import datetime
import logging

import zc.lockfile

from . import timing

# disable the error reporting in zc.lockfile because it will
#  just spew errors as we repeatedly attempt to acquire an
#  unavailable lock.
logging.getLogger('zc.lockfile').setLevel(logging.ERROR+1)


class FileLockTimeout(Exception):
    pass

class LockBase(object):
    def __init__(self, timeout=10, delay=.05):
        if isinstance(timeout, numbers.Number):
            timeout = datetime.timedelta(seconds=timeout)
        if isinstance(delay, numbers.Number):
            delay = datetime.timedelta(seconds=delay)
        self.timeout = timeout
        self.delay = delay

    def __enter__(self):
        """
        Acquire the lock unless already locked.
        """
        if not self.is_locked():
            self.acquire()
        return self

    def __exit__(self, type, value, traceback):
        self.release()

    def __del__(self):
        """
        Release the lock on destruction.
        """
        self.release()


class FileLock(LockBase):
    """
    A cross-platform locking file context.

    May be used in a with statement to provide system-level concurrency
    protection.

    This class relies on zc.lockfile for the underlying locking.

    This class is not threadsafe.
    """

    def __init__(self, lockfile, *args, **kwargs):
        """
        Construct a FileLock. Specify the path to the file to lock and
        optionally the maximum timeout and the delay between each attempt to
        lock.

        Timeout and delay can be given in numeric seconds or as
        `datetime.timedelta` objects.
        """
        self.lockfile = lockfile
        super(FileLock, self).__init__(*args, **kwargs)

    def acquire(self):
        """
        Attempt to acquire the lock every `delay` seconds until the
        lock is acquired or until `timeout` has expired.

        Raises FileLockTimeout if the timeout is exceeded.

        Errors opening the lock file (other than if it exists) are
        passed through.
        """
        stopwatch = timing.Stopwatch()
        attempt = functools.partial(zc.lockfile.LockFile, self.lockfile)
        while True:
            try:
                self.lock = attempt()
                break
            except zc.lockfile.LockError:
                timeout_expired = stopwatch.split() >= self.timeout
                if timeout_expired:
                    raise FileLockTimeout()
                time.sleep(self.delay.total_seconds())

    def is_locked(self):
        return hasattr(self, 'lock')

    def release(self):
        """
        Release the lock and delete the lockfile.
        """
        if self.is_locked():
            self.lock.close()
            del self.lock
            os.remove(self.lockfile)


class ExclusiveContext(LockBase):
    """
    An exclusive context on an existing, open file.
    """
    def __init__(self, file, *args, **kwargs):
        """
        file should be an open file
        """
        self.file = file
        super(ExclusiveContext, self).__init__(*args, **kwargs)

    def acquire(self):
        """
        Attempt to acquire the lock every `delay` seconds until the
        lock is acquired or until `timeout` has expired.

        Raises FileLockTimeout if the timeout is exceeded.

        Errors opening the lock file (other than if it exists) are
        passed through.
        """
        stopwatch = timing.Stopwatch()
        attempt = functools.partial(zc.lockfile._lock_file, self.file)
        while True:
            try:
                self.lock = attempt()
                break
            except zc.lockfile.LockError:
                timeout_expired = stopwatch.split() >= self.timeout
                if timeout_expired:
                    raise FileLockTimeout()
                time.sleep(self.delay.total_seconds())

    def is_locked(self):
        return hasattr(self, 'lock')

    def release(self):
        """
        Release the lock and delete the lockfile.
        """
        if self.is_locked():
            zc.lockfile._unlock_file(self.file)
            del self.lock
