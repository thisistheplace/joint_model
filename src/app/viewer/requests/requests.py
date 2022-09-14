import io
import json
import os
import requests

from app.server.worker.jobs.interfaces import MeshJob

from .exceptions import MeshApiHttpError
from ...interfaces import Model, DashVtkModel
from ...interfaces.validation import validate_and_convert_json
from ...constants import RESTAPI_URL
from ...server.worker.jobs.interfaces import MeshJob
from ...server.worker.jobs.job import JobStatus

def _get_url() -> str:
    if RESTAPI_URL not in os.environ:
        raise OSError(f"Environment variable {RESTAPI_URL} is not defined")
    return os.environ[RESTAPI_URL]

async def submit_job(model: Model) -> MeshJob:
    """Makes a request to server hosting FastAPI

    Uses environment variable VTK_MESHER_URL to make request.

    Returns:
        DashVtkModel returned from response
    """
    # os.environ[RESTAPI_URL] = "http://127.0.0.1:8000"
    url = _get_url()
    json_model = validate_and_convert_json(model, Model)
    with requests.post(f"{url}/meshmodel/submit", json=json_model.dict()) as r:
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise MeshApiHttpError(r)
        job_str = r.content.decode("utf-8")
        return MeshJob(**json.loads(job_str))

async def monitor_job(job: MeshJob) -> MeshJob:
    """Gets the status of a job which has been submitted"""
    url = _get_url()
    with requests.get(f"{url}/meshmodel/monitor/{job.id}") as r:
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise MeshApiHttpError(r)
        job_str = r.content.decode("utf-8")
    return MeshJob(**json.loads(job_str))

async def get_mesh(job: MeshJob) -> DashVtkModel:
    """Gets the mesh from a server hosting Joint Mesh FastAPI

    Uses environment variable VTK_MESHER_URL to make request.

    Returns:
        DashVtkModel returned from response
    """
    # os.environ[RESTAPI_URL] = "http://127.0.0.1:8000"
    url = _get_url()
    out = io.BytesIO()
    with requests.get(f"{url}/meshmodel/mesh/{job.id}", stream=True) as r:
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise MeshApiHttpError(r)

        for chunk in r.iter_content(chunk_size=8192):
            # If you have chunk encoded response uncomment if
            # and set chunk_size parameter to None.
            # if chunk:
            out.write(chunk)
    out.seek(0)

    json_out = json.loads(out.read().decode("utf-8"))
    return DashVtkModel.parse_obj(json_out)
