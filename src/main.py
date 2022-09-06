from fastapi import FastAPI

import os

from app.constants import VIEWER_URL, RESTAPI_URL
from app.server.routers import home, meshing
from app.server.worker.worker import Worker

app = FastAPI()
app.include_router(home.router)
app.include_router(meshing.router)

# setup workers
worker = Worker()
worker.start()

# check environment variable
if VIEWER_URL not in os.environ:
    raise OSError(f"Environment variable {VIEWER_URL} is not defined")
if RESTAPI_URL not in os.environ:
    raise OSError(f"Environment variable {RESTAPI_URL} is not defined")