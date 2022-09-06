import io
import os
import requests

from ...constants import RESTAPI_URL
from ...interfaces.examples.joints import EXAMPLE_JOINTS


async def get_mesh(option: str) -> str:
    """Makes a request to server hosting FastAPI

    Uses environment variable VTK_MESHER_URL to make request.

    Returns:
        String of VTK data returned from response
    """
    if option not in EXAMPLE_JOINTS:
        raise KeyError(f"Model {option} is not in the available models!")

    if RESTAPI_URL not in os.environ:
        raise OSError(f"Environment variable {RESTAPI_URL} is not defined")
    url = os.environ[RESTAPI_URL]

    out = io.BytesIO()
    with requests.get(f"{url}/examples/{option}", stream=True) as r:
        r.raise_for_status()
        for chunk in r.iter_content(chunk_size=8192):
            # If you have chunk encoded response uncomment if
            # and set chunk_size parameter to None.
            # if chunk:
            out.write(chunk)
    out.seek(0)

    return out.read()
