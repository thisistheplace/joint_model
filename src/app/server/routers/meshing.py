from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

import io
import json

from app.converters.encoder import NpEncoder
from app.interfaces.examples.joints import EXAMPLE_JOINTS
from app.server.worker.worker import run_job, Worker
from app.server.worker.job import Job

from ...interfaces import Joint, Model
from ...interfaces.examples.joints import EXAMPLE_JOINTS

router = APIRouter()
# get worker singleton
worker = Worker()

def do_meshing(joint: Joint) -> StreamingResponse:
    job = Job(joint)
    try:
        job = run_job(worker, job)

        def iterfile():
            with io.StringIO() as file_like:
                json.dump(job.mesh, file_like, cls=NpEncoder)
                file_like.seek(0)
                yield from file_like

        return StreamingResponse(iterfile(), media_type="application/json")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error while generating mesh: {e}")

@router.get("/examples/{jointname}")
def mesh_example(jointname: str):
    if jointname not in EXAMPLE_JOINTS:
        raise HTTPException(
            status_code=404, detail=f"Joint model {jointname} not found"
        )
    return do_meshing(EXAMPLE_JOINTS[jointname])

@router.post("/meshmodel")
def mesh_model(model: Model):
    # do some validation here!
    return do_meshing(model.joint)