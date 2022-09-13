"""Methods for accessing job data"""
from fastapi import HTTPException
from fastapi.responses import StreamingResponse

import io
import json

from app.converters.encoder import NpEncoder
from app.server.worker.worker import run_job, Worker
from app.server.worker.jobs.job import Job, JobStatus
from app.server.worker.jobs.interfaces import MeshJob

from ....interfaces import Model
from ....interfaces.examples.joints import EXAMPLE_MODELS

# get worker singleton
worker = Worker()

def submit_job(model: Model) -> MeshJob:
    job: Job = Job(model)
    worker.inqueue.put(job)
    return MeshJob(
        id=job.id,
        status=JobStatus.Pending
    )

def monitor_job(id: str) -> MeshJob:
    job = Job(model)
    try:
        job = run_job(worker, job)

        def iterfile():
            with io.StringIO() as file_like:
                json.dump(job.mesh.dict(), file_like, cls=NpEncoder)
                file_like.seek(0)
                yield from file_like

        return StreamingResponse(iterfile(), media_type="application/json")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error while generating mesh: {e}")

def get_job(id: str) -> StreamingResponse:
    job = Job(model)
    try:
        job = run_job(worker, job)

        def iterfile():
            with io.StringIO() as file_like:
                json.dump(job.mesh.dict(), file_like, cls=NpEncoder)
                file_like.seek(0)
                yield from file_like

        return StreamingResponse(iterfile(), media_type="application/json")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error while generating mesh: {e}")