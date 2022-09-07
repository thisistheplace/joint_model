from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

import io
import json

from app.converters.encoder import NpEncoder
from app.interfaces.examples.joints import EXAMPLE_MODELS
from app.server.worker.worker import run_job, Worker
from app.server.worker.job import Job

from ...interfaces import Model
from ...interfaces.examples.joints import EXAMPLE_MODELS

router = APIRouter()
# get worker singleton
worker = Worker()


def do_meshing(model: Model) -> StreamingResponse:
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


@router.get("/examples/{modelname}")
def mesh_example(modelname: str):
    if modelname not in EXAMPLE_MODELS:
        raise HTTPException(
            status_code=404, detail=f"Joint model {modelname} not found"
        )
    return do_meshing(EXAMPLE_MODELS[modelname])


@router.post("/meshmodel")
def mesh_joint_model(model: Model):
    # do some validation here!
    return do_meshing(model)
