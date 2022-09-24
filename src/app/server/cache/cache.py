"""Threadsafe dictionary accessors"""
from contextlib import contextmanager
import copy
import threading

from ..singleton import Singleton
from ..worker.jobs.job import Job, JobStatus


class Cache(Singleton):
    def __init__(self):
        super(Cache, self).__init__()
        if not hasattr(self, "_data"):
            self._data: dict[str, Job] = {}
            self._lock = threading.RLock()

    @property
    @contextmanager
    def store(self) -> dict[str, Job]:
        with self._lock:
            yield self._data


def store_job(job: Job):
    cache = Cache()  # singleton
    with cache.store as store:
        store[job.id] = job


def get_job(job_id: str):
    cache = Cache()  # singleton
    with cache.store as store:
        if job_id not in store:
            not_found = Job(None, job_id)
            not_found.status = JobStatus.NOTFOUND
            return not_found
        return copy.deepcopy(store[job_id])
