from multiprocessing import Queue, Event, RLock, Condition
import queue

from .jobs.job import Job, JobStatus
from ...converters.model import convert_model_to_dash_vtk
from ..singleton import SingletonProcess

SENTINEL = "STOP"
DELAY = 5  # ms


class WorkerException(Exception):
    pass

class Worker(SingletonProcess):
    def __init__(self):
        super(Worker, self).__init__()
        if not hasattr(self, "_inqueue"):
            self._inqueue = Queue()
            self._outqueue = Queue()
            self._stop_event = Event()
            self._lock = RLock()
            self._notify = Condition()

    @property
    def inqueue(self):
        return self._inqueue

    @property
    def outqueue(self):
        return self._outqueue

    def submit(self, job: Job) -> Job:
        with self._lock:
            job.status = JobStatus.SUBMITTED
            self.inqueue.put(job)
            return job

    def start(self, *args, **kwargs):
        if self.is_alive():
            raise WorkerException(
                "Worker is currently running, please call self.stop() before starting"
            )
        self._stop_event.clear()
        super(Worker, self).start(*args, **kwargs)

    def stop(self):
        with self._lock:
            if not self._stop_event.is_set():
                self._stop_event.set()

            while self.inqueue.qsize() > 0:
                self.inqueue.get_nowait()
            self.inqueue.put(SENTINEL)
            with self._notify:
                self._notify.wait()

            if self.is_alive():
                self.join()
            while self.outqueue.qsize() > 0:
                self.outqueue.get_nowait()
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
                with self._notify:
                    self._notify.notify_all()
                break

            elif not isinstance(job, Job):
                # skip since this isn't a valid object
                continue

            elif job.status != JobStatus.SUBMITTED:
                continue

            try:
                job.mesh = convert_model_to_dash_vtk(job.data)
                job.status = JobStatus.COMPLETE
            except Exception as e:
                print(str(e))
                job.error = str(e)
                job.status = JobStatus.ERROR
            self.outqueue.put(job)