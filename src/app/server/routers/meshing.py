from fastapi import APIRouter, HTTPException

from ..worker.jobs.interfaces import MeshJob
from ..worker.manager import Manager

from ...interfaces import Model
from ...interfaces.examples.joints import EXAMPLE_MODELS

router = APIRouter()
manager = Manager()


@router.get("/examples/{modelname}")
def mesh_example(modelname: str):
    if modelname not in EXAMPLE_MODELS:
        raise HTTPException(
            status_code=404, detail=f"Joint model {modelname} not found"
        )
    return manager.submit_job(EXAMPLE_MODELS[modelname])


@router.post("/meshmodel/submit", response_model=MeshJob)
def submit_model_to_mesher(model: Model):
    # do some validation here!
    return manager.submit_job(model)


@router.get("/meshmodel/monitor/{job_id}", response_model=MeshJob)
def get_job_status(job_id: str):
    return manager.monitor_job(job_id)


@router.get("/meshmodel/mesh/{job_id}")
def get_model_from_mesher(job_id: str):
    return manager.get_job(job_id)
