from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

import os

from .constants import VIEWER_URL, RESTAPI_URL
from .server.routers import home, meshing
from .server.worker.manager import Manager

# check environment variable
if VIEWER_URL not in os.environ:
    raise OSError(f"Environment variable {VIEWER_URL} is not defined")
if RESTAPI_URL not in os.environ:
    raise OSError(f"Environment variable {RESTAPI_URL} is not defined")

app = FastAPI()
app.include_router(home.router)
app.include_router(meshing.router)
app.mount("/static", StaticFiles(directory="static"), name="static")

# setup manager with workers
manager = Manager()
manager.start()


@app.on_event("shutdown")
def shutdown_event():
    manager.stop()
