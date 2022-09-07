from fastapi import APIRouter, BackgroundTasks
from fastapi.responses import HTMLResponse

import os

from .pingviewer import ping_viewer
from app.constants import VIEWER_URL, RESTAPI_URL, GITHUB_URL

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def root(background_tasks: BackgroundTasks):
    # Wake up viewer service by pinging it
    # background_tasks.add_task(ping_viewer)

    url_example = f"{os.environ[RESTAPI_URL]}/examples/TJoint"
    url_docs = f"{os.environ[RESTAPI_URL]}/redoc"
    url_viewer = os.environ[VIEWER_URL]
    html_content = f"""
    <html>
        <head>
            <title>Joint Meshing REST API</title>
            <meta name="viewport" content="width=device-width" />
            <!--using same theme as Dash Flatly-->
            <link href="https://cdn.jsdelivr.net/npm/bootswatch@5.2.0/dist/flatly/bootstrap.min.css" rel="stylesheet">
            <link href="/static/css/custom.css" rel="stylesheet">
        </head>
        <body>
            <div class="maincontent">
                <div class="container fullwidth">
                    <h1 sty>Joint Meshing REST API</h1>
                    <div class="row rowfont"> 
                        <div class="col-lg-4 col-md-12 padcard">
                            <div class="card text-white bg-primary mb-3" style="max-width: 20rem; height: 100%;">
                                <div class="card-header">REST API</div>
                                <div class="card-body">
                                    <h4 class="card-title">Create joint meshes</h4>
                                    <p class="card-text">A REST API to generate joint meshes from beam element models, input using json format.</p>
                                    <p class="card-text">This REST API is developed using <a href='https://fastapi.tiangolo.com'>FastAPI</a>. Read the docs for endpoints and schemas.</p>
                                    <div class="padbutton">
                                        <button type="button" onclick="location.href='{url_docs}'" class="btn btn-success btn-lg">Docs</button>
                                    </div>
                                    <div class="padbutton">
                                        <button type="button" onclick="location.href='{url_example}'" class="btn btn-success btn-lg">Example response</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="col-lg-4 col-md-12 padcard">
                            <div class="card text-white bg-primary mb-3" style="max-width: 20rem; height: 100%;">
                                <div class="card-header">Viewer</div>
                                <div class="card-body">
                                    <h4 class="card-title">View joint meshes</h4>
                                    <p class="card-text">A user interface for creating <b>and</b> viewing joint meshes. This uses the REST API to perform the meshing.</p>
                                    <p class="card-text">This viewer is developed using the <a href='https://dash.plotly.com/vtk'>Dash VTK</a> python package.</p>
                                    <div class="padbutton">
                                        <button type="button" onclick="location.href='{url_viewer}'" class="btn btn-success btn-lg">Viewer</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="logos">
                        <button type="button" onclick="location.href='{GITHUB_URL}'" class="btn btn-light"><img src="static/img/GitHub-Mark-32px.png"></button>
                    </div>
                </div>
                <div class="fillbottom">
                    <div class="credits">
                        <span class="badge bg-light"><i>Templates by <a href='https://bootswatch.com/flatly'>https://bootswatch.com/flatly</a> :)</span>
                    </div>
                </div>
            </div>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)
