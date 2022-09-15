import queue
import threading
import time

from .jobs.job import Job
from .worker import DELAY, Worker
from ..cache.cache import store_job, get_job

class RunJob(threading.Thread):
    def __init__(self, worker: Worker, job: Job, run: bool = False):
        super(RunJob, self).__init__()
        self._stop = threading.Event()
        self._worker = worker
        self._id = job.id
        store_job(job)
        if run:
            self.start()

    @property
    def job(self):
        """Copy of job in store"""
        return get_job(self._id)

    def stop(self):
        self._stop.set()
        while self.is_alive():
            pass

    def run(self):
        job = self.job
        if not self._worker.is_alive():
            msg = "Worker performing gmsh operations is not running, please contact the administrator"
            job.error = msg
            store_job(job)
            return

        job = self._worker.submit(job)
        store_job(job)

        while True:
            if self._stop.is_set():
                return
            try:
                output = self._worker.outqueue.get()
                if output.id == self._id:
                    store_job(job)
                    return
                self._worker.outqueue.put(job)
            except queue.Empty:
                pass
            time.sleep(DELAY / 1000.0)