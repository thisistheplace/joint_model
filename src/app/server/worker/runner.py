import queue
import threading

from .jobs.job import Job
from .worker import DELAY, Worker
from ..cache.cache import store_job, get_job

class RunJob(threading.Thread):
    def __init__(self, worker: Worker, job: Job, run: bool = False):
        super(RunJob, self).__init__()
        self._stop_event = threading.Event()
        self._worker = worker
        self._id = job.id
        self._notify = threading.Condition()
        store_job(job)
        if run:
            self.start()

    @property
    def job(self) -> Job:
        """Copy of job in store"""
        return get_job(self._id)

    @property
    def notification(self) -> threading.Condition:
        return self._notify

    def wait(self) -> Job:
        with self.notification:
            self.notification.wait(120)
        return get_job(self.job.id)

    def stop(self):
        self._stop_event.set()
        if self.is_alive():
            self.join()
        with self.notification:
            self.notification.notify_all()

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
            if self._stop_event.is_set():
                break
            try:
                # TODO: use nowait so we can interrupt runner at some point
                output = self._worker.outqueue.get()
                if output.id == self._id:
                    store_job(output)
                    with self.notification:
                        self.notification.notify_all()
                    return
                self._worker.outqueue.put(output)
            except queue.Empty:
                pass
            # time.sleep(DELAY / 1000.0)