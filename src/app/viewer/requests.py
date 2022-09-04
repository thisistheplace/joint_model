import io
import os
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
    
    out = io.BytesIO()
    with requests.get(f"{url}/{option}", stream=True) as r:
        r.raise_for_status()
        for chunk in r.iter_content(chunk_size=8192):
            print("reading chunk")
            # If you have chunk encoded response uncomment if
            # and set chunk_size parameter to None.
            #if chunk: 
            out.write(chunk)
        print("finished")
    out.seek(0)

    return out.read()