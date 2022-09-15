from fastapi import APIRouter, HTTPException

from app.interfaces.examples.joints import EXAMPLE_MODELS
from app.server.worker.worker import Worker

from ..worker.jobs.interfaces import MeshJob
from ..worker.management import submit_job, get_job, monitor_job

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

@router.get("/meshmodel/monitor/{job_id}", response_model=MeshJob)
def get_job_status(job_id: str):
    return monitor_job(job_id)

@router.get("/meshmodel/mesh/{job_id}")
def get_model_from_mesher(job_id: str):
    return get_job(job_id)