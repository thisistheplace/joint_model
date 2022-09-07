import io
import json
import os
import requests

from .exceptions import MeshApiHttpError
from ...interfaces import Model, DashVtkModel
from ...interfaces.validation import validate_and_convert_json
from ...constants import RESTAPI_URL


async def get_mesh(model: Model) -> DashVtkModel:
    """Makes a request to server hosting FastAPI

    Uses environment variable VTK_MESHER_URL to make request.

    Returns:
        DashVtkModel returned from response
    """
    # os.environ[RESTAPI_URL] = "http://127.0.0.1:8000"
    if RESTAPI_URL not in os.environ:
        raise OSError(f"Environment variable {RESTAPI_URL} is not defined")
    url = os.environ[RESTAPI_URL]

    json_model = validate_and_convert_json(model, Model)
    json_data = json.loads(json_model.json())

    out = io.BytesIO()
    with requests.post(f"{url}/meshmodel", json=json_data, stream=True) as r:
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
