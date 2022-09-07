import os
import requests
from requests.adapters import HTTPAdapter, Retry

from ...constants import VIEWER_URL

def ping_viewer():
    sesh = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[ 502, 503, 504 ])
    sesh.mount('http://', HTTPAdapter(max_retries=retries))
    sesh.get(f"{os.environ[VIEWER_URL]}/ping")