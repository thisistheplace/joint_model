from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

import io
import json

from app.converters.encoder import NpEncoder
from app.interfaces.examples.joints import EXAMPLE_MODELS
from app.server.worker.worker import run_job, Worker
from app.server.worker.jobs.job import Job

from ..worker.jobs.interfaces import MeshJob
from ..worker.jobs.management import submit_job, get_job, monitor_job

from ...interfaces import Model
from ...interfaces.examples.joints import EXAMPLE_MODELS

router = APIRouter()
# get worker singleton
worker = Worker()

@router.get("/examples/{modelname}")
def mesh_example(modelname: str):
    if modelname not in EXAMPLE_MODELS:
        raise HTTPException(
            status_code=404, detail=f"Joint model {modelname} not found"
        )
    return submit_job(EXAMPLE_MODELS[modelname])

@router.post("/meshmodel/submit", response_model=MeshJob)
def submit_model_to_mesher(model: Model):
    # do some validation here!
    return submit_job(model)

@router.get("/meshmodel/monitor", response_model=MeshJob)
def monitor_job(job_id: str):
    return monitor_job(job_id)

@router.get("/meshmodel/mesh")
def get_model_from_mesher(job_id: str):
    return get_job(job_id)