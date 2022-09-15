"""Methods for accessing job data"""
from fastapi import HTTPException
from fastapi.responses import StreamingResponse

import io
import json

from app.converters.encoder import NpEncoder
from app.server.worker.worker import Worker
from app.server.worker.jobs.job import Job, JobStatus
from app.server.worker.jobs.interfaces import MeshJob

from .runner import RunJob
from ..singleton import Singleton
from ..cache.cache import Cache, store_job, get_job
from ...interfaces import Model
from ...interfaces.examples.joints import EXAMPLE_MODELS


class Manager(Singleton):
    """Submit and monitor jobs"""
    def __init__(self):
        self._cache = Cache() # singleton
        self._runners = [] # hold runner threads
        self._worker = Worker() # singleton

    @property
    def runners(self):
        return self._runners

    @property
    def worker(self):
        return self._worker

    def start(self):
        if not self.worker.is_alive():
            self.worker.start()

    def stop(self):
        for runner in self.runners:
            runner.stop()
        self._runners = []
        self.worker.stop()

    def submit_job(self, model: Model) -> MeshJob:
        job: Job = Job(model)
        self._runners.append(RunJob(self.worker, job, True))
        return MeshJob(
            id=job.id,
            status=JobStatus.SUBMITTED
        )

    def monitor_job(self, id: str) -> MeshJob:
        try:
            return MeshJob(
                id=id,
                status=get_job(id)
            )
        except KeyError:
            return MeshJob(
                id=id,
                status=JobStatus.NOTFOUND
            )

    def get_job(self, id: str) -> StreamingResponse:
        job = get_job(id)
        if job.status == JobStatus.ERROR:
            raise HTTPException(status_code=500, detail=f"Error while generating mesh: {job.error}")
        elif job.status == JobStatus.COMPLETE:
            try:
                def iterfile():
                    with io.StringIO() as file_like:
                        json.dump(job.mesh.dict(), file_like, cls=NpEncoder)
                        file_like.seek(0)
                        yield from file_like

                return StreamingResponse(iterfile(), media_type="application/json")
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error while generating mesh: {e}")
        else:
            raise HTTPException(status_code=500, detail=f"Job is not complete, current status is: {job.status}")