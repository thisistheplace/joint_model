from multiprocessing import Process, Queue, Event, RLock
import time

from .job import Job, JobStatus
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
        self._stop_event = Event()
        self._lock = RLock()

    @property
    def inqueue(self):
        return self._inqueue

    @property
    def outqueue(self):
        return self._outqueue

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

            elif job.status != JobStatus.PENDING:
                continue

            # Mesh object if pending
            job.status = JobStatus.RUNNING

            try:
                job.mesh = convert_model_to_dash_vtk(job.data)
                job.status = JobStatus.COMPLETE
            except Exception as e:
                job.error = str(e)

            self.outqueue.put(job)


def run_job(worker: Worker, job: Job):
    if not worker.is_alive():
        raise WorkerException(
            "Worker performing gmsh operations is not running, please contact the administrator"
        )

    worker.inqueue.put(job)

    output = worker.outqueue.get(timeout=60.0)
    while output.id != job.id:
        time.sleep(DELAY / 1000.0)
        output = worker.outqueue.get(timeout=60.0)

    if output.error is not None or output.status != JobStatus.COMPLETE:
        raise WorkerException(f"Error occurred while processing mesh: {output.error}")
    return output
