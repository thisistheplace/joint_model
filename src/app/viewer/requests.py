import os
from urllib.error import HTTPError
import requests

from .constants import ENDPOINT
from .models import DEMO_MODELS

async def get_vtk_mesh(option: str) -> str:
    """Makes a request to server hosting FastAPI
    
    Uses environment variable VTK_MESHER_URL to make request.

    Returns:
        String of VTK data returned from response
    """
    if option not in DEMO_MODELS:
        raise KeyError(f"Model {option} is not in the available models!")
    
    if ENDPOINT not in os.environ:
        raise OSError(f"Environment variable {ENDPOINT} is not defined")
    url = os.environ[ENDPOINT]
    requests.Response
    response = requests.get(url, data=DEMO_MODELS[option])

    if response.status_code != requests.codes["ok"]:
        raise HTTPError(url, response.status_code, response.text)
    
    return response.content