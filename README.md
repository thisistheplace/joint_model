![Test status](https://github.com/thisistheplace/joint_model/actions/workflows/test.yml/badge.svg?event=push)

# Joint Meshing API
Generate shell mesh representations of 3D joints to DNV RP-C203 for performing fatigue assessments.

## Components
### REST API
The guts of this project are deployed as a service which can be accessed via a REST API. The REST API
is developed using [FastAPI](https://fastapi.tiangolo.com) with backend meshing completed using [gmsh](https://gmsh.info).

This API is deployed here: [https://rest.jointmesh.beancandesign.com](https://rest.jointmesh.beancandesign.com)

### Viewer
Meshes produced by the REST API can be viewed using a web-based visualizer developed using [Dash VTK](https://dash.plotly.com/vtk). This allows users to input .json or pick examples and interrogate the
generated meshes.

This Viewer is deployed here: [https://viewer.jointmesh.beancandesign.com](https://viewer.jointmesh.beancandesign.com)

## Building the components
### Docker Desktop
The REST API and Viewer can be deployed locally using `ubuntu` images run on Docker Desktop by executing:

```
bash build.sh
```

The REST API will then be hosted at [http://127.0.0.1:8000](http://127.0.0.1:8000) and the Viewer
will be hosted at [http://127.0.0.1:8050](http://127.0.0.1:8000).

Edit the [docker-compose.yml](docker-compose.yml) file directly to change the port numbers etc.

### Cloud Run
Dockerfiles are provided for each component which can be used to run the services separately using
a cloud service provider:
- Build the REST API using [Dockerfile-rest](Dockerfile-rest)
- Build the Viewer using [Dockerfile-viewer](Dockerfile-viewer)

> Note: set the URLs of the viewer in the containers using environment variables `RESTAPI_URL` and `VIEWER_URL`

# Testing
Tests are written using [pytest](https://docs.pytest.org). To run the tests in `docker` execute:

```
bash test.sh
```

# License
The Joint Meshing API is distributed under the terms of the [GNU General Public License (GPL)](LICENSE).