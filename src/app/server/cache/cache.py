"""Threadsafe dictionary accessors"""
from contextlib import contextmanager
import copy
import threading

from ..singleton import Singleton
from ..worker.jobs.job import Job, JobStatus

class Cache(Singleton):
    def __init__(self):
        self._data: dict[str, Job] = {}
        self._lock = threading.RLock()
    
    @contextmanager
    @property
    def store(self) -> dict[str, Job]:
        with self._lock:
            yield self._data

def store_job(job: Job):
    cache = Cache() # singleton
    with cache.store as store:
        store[job.id] = job

def get_job(id: str):
    cache = Cache() # singleton
    with cache.store as store:
        if id not in store:
            not_found =  Job(None, id)
            not_found.status = JobStatus.NOTFOUND
            return not_found
        return copy.deepcopy(store[id])