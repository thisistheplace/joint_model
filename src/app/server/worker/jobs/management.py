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
    worker.submit(job)
    return MeshJob(
        id=job.id,
        status=JobStatus.SUBMITTED
    )

def monitor_job(id: str) -> MeshJob:
    return MeshJob(
        id=id,
        status=worker.job_status(id)
    )

def get_job(id: str) -> StreamingResponse:
    status = worker.job_status(id)
    if status == JobStatus.ERROR:
        job = worker.get_complete(id)
        if job is not None:
            raise HTTPException(status_code=500, detail=f"Error while generating mesh: {job.error}")
        else:
            raise HTTPException(status_code=500, detail=f"Could not find job: {job.id}")
    elif status == JobStatus.COMPLETE:
        try:
            job = worker.get_complete(id)
            def iterfile():
                with io.StringIO() as file_like:
                    json.dump(job.mesh.dict(), file_like, cls=NpEncoder)
                    file_like.seek(0)
                    yield from file_like

            return StreamingResponse(iterfile(), media_type="application/json")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error while generating mesh: {e}")
    else:
        raise HTTPException(status_code=500, detail=f"Job is not complete, current status is: {status}")