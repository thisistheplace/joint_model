from fastapi import APIRouter, BackgroundTasks
from fastapi.responses import HTMLResponse

import requests
import os

from app.constants import VIEWER_URL, RESTAPI_URL

router = APIRouter()

def ping_viewer():
    requests.get(VIEWER_URL)

@router.get("/", response_class=HTMLResponse)
async def root(background_tasks: BackgroundTasks):
    # Wake up viewer service by pinging it
    background_tasks.add_task(ping_viewer)

    url_example = f"{os.environ[RESTAPI_URL]}/examples/TJoint"
    url_docs = f"{os.environ[RESTAPI_URL]}/docs"
    url_viewer = f"{os.environ[VIEWER_URL]}"
    html_content = f"""
    <html>
        <head>
            <title>Joint Meshing API</title>
            <!--using same theme as Dash Flatly-->
            <link href="https://cdn.jsdelivr.net/npm/bootswatch@5.2.0/dist/flatly/bootstrap.min.css" rel="stylesheet">
            <style>
            body {{
                padding: 80px
            }}
            h1 {{
                padding-bottom: 40px
            }}
            .padbutton {{
                padding-top: 5px;
                padding-bottom: 5px;
            }}
            </style>
        </head>
        <body>
            <h1 sty>Joint Meshing API</h1>
            <div class="row"> 
                <div class="col-lg-4">
                    <div class="card text-white bg-primary mb-3" style="max-width: 20rem;">
                        <div class="card-header">RestAPI</div>
                        <div class="card-body">
                            <h4 class="card-title">Create joint meshes</h4>
                            <p class="card-text">A RestAPI is available to generate joint meshes from json input.</p>
                            <p class="card-text">This RestAPI is developed using <a href='https://fastapi.tiangolo.com'>FastAPI</a>.</p>
                            <div class="padbutton">
                                <button type="button" onclick="location.href='{url_docs}'" class="btn btn-success btn-lg">Docs</button>
                            </div>
                            <div class="padbutton">
                                <button type="button" onclick="location.href='{url_example}'" class="btn btn-success btn-lg">Example response</button>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-lg-4">
                    <div class="card text-white bg-primary mb-3" style="max-width: 20rem;">
                        <div class="card-header">Viewer</div>
                        <div class="card-body">
                            <h4 class="card-title">View joint meshes</h4>
                            <p class="card-text">You can also create <b>and</b> view joint meshes using a user interface.</p>
                            <p class="card-text">This viewer is developed using <a href='https://dash.plotly.com/vtk'>Dash VTK</a>.</p>
                            <div class="padbutton">
                                <button type="button" onclick="location.href='{url_viewer}'" class="btn btn-success btn-lg">Viewer</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)