from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pathlib import Path
import os
import io
import shutil
import uuid

from .viewer.models import DEMO_MODELS
from .converters.model  import mesh_model

app = FastAPI()

def tempdir():
    temp_path = Path(uuid.uuid4()).resolve()
    os.makedirs(temp_path)
    yield temp_path
    shutil.rmtree(temp_path)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/meshjoint/{jointname}")
def mesh_joint(jointname):
    if jointname not in DEMO_MODELS:
        raise HTTPException(status_code=404, detail=f"Joint model {jointname} not found")

    model_data = DEMO_MODELS[jointname]
    mesh = mesh_model(model_data)

    with tempdir() as temp:
        out = io.FileIO(str(temp / "test.vtk"), "wb+")
        mesh.write(out, "vtk")
        out.seek(0)
        return StreamingResponse(out, media_type="application/octet-stream")