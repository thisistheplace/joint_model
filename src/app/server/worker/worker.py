from multiprocessing import Process, Queue, Event, RLock
import time

from .jobs.job import Job, JobStatus
from ...converters.model import convert_model_to_dash_vtk

SENTINEL = "STOP"
DELAY = 5  # ms


class WorkerException(Exception):
    pass


class SingletonProcess(Process):
    def __new__(cls, *args, **kwds):
        it = cls.__dict__.get("__it__")
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)
        it.init(*args, **kwds)
        return it

    def init(self, *args, **kwds):
        super(SingletonProcess, self).__init__()


class Worker(SingletonProcess):
    def __init__(self):
        super(Worker, self).__init__()
        self._inqueue = Queue()
        self._outqueue = Queue()
        self._pending = Queue()
        self._stop_event = Event()
        self._lock = RLock()

    @property
    def inqueue(self):
        return self._inqueue

    @property
    def outqueue(self):
        return self._outqueue

    def submit(self, job: Job):
        with self._lock:
            job.status = JobStatus.SUBMITTED
            self._pending.put(job)
            self.inqueue.put(job)

    def get_complete(self, id: str) -> Job:
        with self._lock:
            status = self.job_status(id)
            if status in [JobStatus.COMPLETE, JobStatus.ERROR]:
                jobs = []
                found = None
                while self.outqueue.qsize() > 0:
                    job = self.outqueue.get_nowait()
                    if job.id == id:
                        found = job
                        break
                    jobs.append(job)
                for other_job in jobs:
                    self.outqueue.put(other_job)
                return found

    def _update_job_status(self, id: str, status: JobStatus):
        with self._lock:
            jobs = []
            while self._pending.qsize() > 0:
                job = self._pending.get_nowait()
                if job.id == id:
                    job.status = status
                jobs.append(job)
            for job in jobs:
                self._pending.put(job)

    def _complete_job(self, job: Job, status: JobStatus):
        with self._lock:
            pending_jobs = []
            while self._pending.qsize() > 0:
                pending = self._pending.get_nowait()
                if pending.id == job.id:
                    break
                else:
                    pending_jobs.append(pending)
            job.status = status
            self.outqueue.put(job)
            for pending in pending_jobs:
                self._pending.put(pending)

    def job_status(self, id: str) -> JobStatus:
        with self._lock:
            jobs = []
            job_status = None
            while self._pending.qsize() > 0:
                job = self._pending.get_nowait()
                if job.id == id:
                    job_status = job.status
                jobs.append(job)
            for job in jobs:
                self._pending.put(job)
            if job_status is None:
                jobs = []
                while self.outqueue.qsize() > 0:
                    job = self.outqueue.get_nowait()
                    if job.id == id:
                        job_status = job.status
                    jobs.append(job)
                for job in jobs:
                    self.outqueue.put(job)
            if job_status is None:
                return JobStatus.NOTFOUND
            return job_status

    def start(self, *args, **kwargs):
        if self.is_alive():
            raise WorkerException(
                "Worker is currently running, please call self.stop() before starting"
            )
        super(Worker, self).start(*args, **kwargs)

    def stop(self):
        with self._lock:
            if not self._stop_event.is_set():
                self._stop_event.set()
            # empty inqueue
            while self.inqueue.qsize() > 0:
                self.inqueue.get_nowait()
            self.inqueue.put(SENTINEL)
            if self.is_alive():
                self.join()
            while self.is_alive():
                time.sleep(DELAY / 1000)
            while self._pending.qsize() > 0:
                self._pending.get_nowait()
            self.close()
            del self

    def run(self):
        while True:
            if self._stop_event.is_set():
                break

            # pull an item from the queue
            job = self.inqueue.get()

            # check if stop is requested
            if job == SENTINEL:
                # stop event to notify other threads
                if not self._stop_event.is_set():
                    self._stop_event.set()
                break

            elif not isinstance(job, Job):
                # skip since this isn't a valid object
                continue

            elif job.status != JobStatus.SUBMITTED:
                continue

            # Mesh object if pending
            self._update_job_status(job.id, JobStatus.RUNNING)

            try:
                job.mesh = convert_model_to_dash_vtk(job.data)
                self._complete_job(job, JobStatus.COMPLETE)
            except Exception as e:
                job.error = str(e)
                self._complete_job(job, JobStatus.ERROR)


def run_job(worker: Worker, job: Job):
    if not worker.is_alive():
        raise WorkerException(
            "Worker performing gmsh operations is not running, please contact the administrator"
        )

    worker.submit(job)

    output = worker.outqueue.get(timeout=60.0)
    while output.id != job.id:
        worker.outqueue.put(job)
        time.sleep(DELAY / 1000.0)
        output = worker.outqueue.get(timeout=60.0)

    if output.error is not None or output.status != JobStatus.COMPLETE:
        raise WorkerException(f"Error occurred while processing mesh: {output.error}")
    return output
