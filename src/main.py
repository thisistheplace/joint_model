from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse

from contextlib import contextmanager
import io
import json

from app.converters.encoder import NpEncoder
from app.viewer.models import DEMO_MODELS
from app.worker.worker import Worker, run_job
from app.worker.job import Job

app = FastAPI()

# setup workers
worker = Worker()
worker.start()

# @contextmanager
# def jsonstream(data):
#     temp = io.StringIO()
#     json.dump(data, temp)

#     temp.close()
#     try:
#         yield temp.name
#     finally:
#         os.unlink(temp.name)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/meshjoint/{jointname}")
def mesh_joint(jointname):
    if jointname not in DEMO_MODELS:
        raise HTTPException(status_code=404, detail=f"Joint model {jointname} not found")

    job = Job(DEMO_MODELS[jointname])

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