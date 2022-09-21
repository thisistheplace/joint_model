"""Methods for accessing job data"""
from fastapi import HTTPException
from fastapi.responses import StreamingResponse

import io
import json
import threading
import time

from app.converters.encoder import NpEncoder
from app.server.worker.worker import Worker
from app.server.worker.jobs.job import Job, JobStatus
from app.server.worker.jobs.interfaces import MeshJob

from .runner import RunJob
from ..singleton import SingletonThread
from ..cache.cache import Cache,  get_job
from ...interfaces import Model
from ...interfaces.examples.joints import EXAMPLE_MODELS

SENTINEL = "STOP"
DELAY = 5  # ms

class Manager(SingletonThread):
    """Submit and monitor jobs"""
    def __init__(self):
        super(Manager, self).__init__()
        self._cache = Cache() # singleton
        if not hasattr(self, "_runners"):
            self._runners = {} # hold runner threads
        self._worker = Worker() # singleton
        self._stop_event = threading.Event()

    @property
    def runners(self):
        return self._runners

    @property
    def worker(self):
        return self._worker

    def start(self, *args, **kwargs):
        self._worker.start()
        super(Manager, self).start(*args, **kwargs)

    def run(self):
        while True:
            if self._stop_event.is_set():
                break
            if not self._worker.is_alive():
                print("worker not alive")
                # Reset worker singleton
                setattr(Worker, "__it__", None)
                worker = Worker()
                # Set all cached jobs as errors
                with self._cache.store as store:
                    for job in store.values():
                        print(job)
                        if job.status not in [JobStatus.COMPLETE, JobStatus.ERROR, JobStatus.NOTFOUND]:
                            job.error = "Job failed due to worker process crashing"
                        worker.outqueue.put(job)
                self._worker = worker
                self.worker.start()
            time.sleep(DELAY)

    def stop(self):
        for runner in self.runners.values():
            runner.stop()
        self._runners = {}
        self.worker.stop()
        self._stop_event.set()

    def submit_job(self, model: Model) -> MeshJob:
        job: Job = Job(model)
        self._runners[job.id] = RunJob(self.worker, job, True)
        return MeshJob(
            id=job.id,
            status=JobStatus.SUBMITTED
        )

    def monitor_job(self, id: str) -> MeshJob:
        return MeshJob(
            id=id,
            status=get_job(id).status
        )

    def get_job(self, id: str) -> StreamingResponse:
        job = get_job(id)
        print(f"get_job: {job}")
        if job.status == JobStatus.ERROR:
            raise HTTPException(status_code=500, headers={"toast": f"Error while generating mesh: {job.error}"})
        elif job.status == JobStatus.COMPLETE:
            try:
                def iterfile():
                    with io.StringIO() as file_like:
                        json.dump(job.mesh.dict(), file_like, cls=NpEncoder)
                        file_like.seek(0)
                        yield from file_like

                return StreamingResponse(iterfile(), media_type="application/json")
            except Exception as e:
                raise HTTPException(status_code=500, headers={"toast": f"Error while generating mesh: {e}"})
        else:
            raise HTTPException(status_code=500, headers={"toast": f"Job is not complete, current status is: {job.status}"})
    
    def wait_for_job(self, id: str) -> Job:
        try:
            return self.runners[id].wait()
        except KeyError:
            raise KeyError(f"Job with id {id.split('-')[0]} is not running")