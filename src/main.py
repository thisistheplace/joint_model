from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
from pathlib import Path
import os
import shutil

from app.viewer.models import DEMO_MODELS
from app.worker.worker import Worker, run_job
from app.worker.job import Job

app = FastAPI()

# setup workers
worker = Worker()
worker.start()

def tempdir(temp_path: Path):
    os.makedirs(temp_path)
    return temp_path

def rmdir(temp_path: Path):
    if temp_path.exists():
        shutil.rmtree(temp_path)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/meshjoint/{jointname}")
def mesh_joint(jointname, background_tasks: BackgroundTasks):
    if jointname not in DEMO_MODELS:
        raise HTTPException(status_code=404, detail=f"Joint model {jointname} not found")

    job = Job(DEMO_MODELS[jointname])

    try:
        temp_path = tempdir(job.path.parent)
        
        background_tasks.add_task(rmdir, temp_path)

        run_job(worker, job)
        
        def iterfile():
            with open(job.path, mode="rb") as file_like:
                yield from file_like
        
        return StreamingResponse(iterfile(), media_type="application/octet-stream")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error while generating mesh: {e}")