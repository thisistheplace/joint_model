from dash import Output, Input, State, html, dcc, callback, MATCH, no_update
import dash_vtk
import dash_bootstrap_components as dbc

import asyncio
import uuid

from ..ids import Ids
from ..toast import make_toast
from ...gmsh_to_dash import vtk_to_dash
from ...requests.exceptions import MeshApiHttpError
from ...requests.requests import monitor_job, submit_job, get_mesh
from ....interfaces import Model
from ....interfaces.validation import validate_and_convert_json
from ....server.worker.jobs.interfaces import MeshJob
from ....server.worker.jobs.job import JobStatus

LOADING_STYLE = {
    "position": "absolute",
    "zIndex": "10",
    "height": "100vh",
    "width": "100vw",
    "display": "none",
    "background": "white"
}

class VtkMeshViewerAIO(html.Div):

    # Make the ids class a public class
    ids = Ids

    # Define the arguments of the All-in-One component
    def __init__(
        self,
        aio_id: str | None = None,
        children: list | list = list,
        options: list[str] | None = None,
    ):
        """VtkMeshViewerAIO is an All-In-One component which visualizes VTK meshes

        Args:
            options: list of options to add to a dropdown
            generate_mesh: asyncronous callback to generate mesh from options string
        """
        if options is None:
            raise TypeError("options must not be None!")

        if aio_id is None:
            aio_id = str(uuid.uuid4())

        # Define the component's layout
        super().__init__(
            children
            + [  # Equivalent to `html.Div([...])`
                dcc.Interval(
                    id=self.ids.interval(aio_id), interval=1000, max_intervals=0
                ),
                make_toast(id=self.ids.submittoast(aio_id), header="Job submission"),
                make_toast(id=self.ids.monitortoast(aio_id), header="Job monitor"),
                make_toast(id=self.ids.getmeshtoast(aio_id), header="Job complete"),
                dcc.Store(id=self.ids.jsonstore(aio_id)),
                dcc.Store(id=self.ids.jobstore(aio_id)),
                dcc.Store(id=self.ids.jobstatus(aio_id)),
                dcc.Store(id=self.ids.jobcomplete(aio_id)),
                html.Div(
                    id=self.ids.loading(aio_id),
                    children=[
                        dbc.Spinner(
                            color="info",
                            spinner_style={
                                "marginTop": "50vh",
                                "marginLeft": "50vw"
                            }
                        )
                    ],
                    style=LOADING_STYLE
                ),
                html.Div(
                    id=self.ids.vtkholder(aio_id),
                    children=[
                        dash_vtk.View(
                            id=self.ids.vtk(aio_id),
                            background=[
                                255,
                                255,
                                255,
                            ],  # RGB array of floating point values between 0 and 1.
                            # interactorSettings=[...], # Binding of mouse events to camera action (Rotate, Pan, Zoom...)
                            cameraPosition=[
                                0,
                                5,
                                0,
                            ],  # Where the camera should be initially placed in 3D world
                            cameraViewUp=[
                                0,
                                0,
                                1,
                            ],  # Vector to use as your view up for your initial camera
                            cameraParallelProjection=False,  # Should we see our 3D work with perspective or flat with no depth perception
                            triggerRender=0,  # Timestamp meant to trigger a render when different
                            triggerResetCamera=0,  # Timestamp meant to trigger a reset camera when different
                            # clickInfo,                    # Read-only property to retrieve picked representation id and picking information
                            # hoverInfo                     # Read-only property to retrieve picked representation id and picking information
                        ),
                    ],
                    style={"height": "100vh", "width": "100vw"},
                ),
            ],
            style={"height": "100vh", "width": "100vw"},
        )

    # Define this component's stateless pattern-matching callback
    # that will apply to every instance of this component.
    @callback(
        Output(ids.vtk(MATCH), "children"),
        Output(ids.getmeshtoast(MATCH), "is_open"),
        Output(ids.getmeshtoast(MATCH), "children"),
        Output(ids.getmeshtoast(MATCH), "icon"),
        Output(ids.getmeshtoast(MATCH), "duration"),
        Input(ids.jobcomplete(MATCH), "data"),
        State(ids.jsonstore(MATCH), "data"),
        prevent_initial_callback=True
    )
    def _get_mesh(job: dict, json_str: str):
        if job is None:
            return no_update
        job = MeshJob(**job)
        if job.status in [JobStatus.COMPLETE, JobStatus.ERROR]:
            try:
                json_mesh = asyncio.run(get_mesh(job))
                json_model = validate_and_convert_json(json_str, Model)
                return (
                    dash_vtk.GeometryRepresentation(
                        [dash_vtk.GeometryRepresentation(vtk_to_dash(json_mesh))]
                    ),
                    True,
                    f"Meshing successful: {json_model.name} ({job.id.split('-')[0]})",
                    "success",
                    4000
                )
            except MeshApiHttpError as e:
                return no_update, True, e.toast_message, "danger", 10000
            except Exception as e:
                msg = str(e)
                if hasattr(e, "response"):
                    msg = f"{e.response.reason}"
                    if hasattr(e.response, "headers"):
                        msg = f"{e.response.headers['toast']}"
                return no_update, True, msg, "danger", 10000
        if job.status == JobStatus.NOTFOUND:
            return no_update, True, f"Job {job.id} could not be found, please try re-submitting", "danger", 10000
        return no_update

    @callback(
        Output(ids.jobstatus(MATCH), "data"),
        Output(ids.monitortoast(MATCH), "is_open"),
        Output(ids.monitortoast(MATCH), "children"),
        Input(ids.jobstore(MATCH), "data"),
        Input(ids.interval(MATCH), "n_intervals"),
        prevent_initial_callback=True
    )
    def _monitor_job(job: dict, _):
        if job is None:
            return no_update
        job = MeshJob(**job)
        try:
            job: MeshJob = asyncio.run(monitor_job(job))
            return job.dict(), no_update, no_update
        except MeshApiHttpError as e:
            return no_update, True, e.toast_message
        except Exception as e:
            return no_update, True, str(e)

    @callback(
        Output(ids.jobstore(MATCH), "data"),
        Output(ids.submittoast(MATCH), "is_open"),
        Output(ids.submittoast(MATCH), "children"),
        Output(ids.submittoast(MATCH), "icon"),
        Output(ids.submittoast(MATCH), "duration"),
        Input(ids.jsonstore(MATCH), "data"),
        prevent_initial_callback=True,
    )
    def _submit_job_to_mesher(json_str: str):
        if json_str is None:
            return no_update
        try:
            json_model = validate_and_convert_json(json_str, Model)
            job: MeshJob = asyncio.run(submit_job(json_model))
            return job.dict(), True, f"Submitted meshing job: {json_model.name} ({job.id.split('-')[0]})", "success", 4000
        except Exception as e:
            return no_update, True, str(e), "danger", 10000

    @callback(
        Output(ids.interval(MATCH), "max_intervals"),
        Output(ids.loading(MATCH), "style"),
        Output(ids.jobcomplete(MATCH), "data"),
        Input(ids.jobstatus(MATCH), "data"),
        State(ids.interval(MATCH), "max_intervals"),
        prevent_initial_call=True,
    )
    def _manage_spinner(job: dict, state: int):
        if job is None:
            return no_update
        job = MeshJob(**job)
        if job.status in [JobStatus.COMPLETE, JobStatus.ERROR, JobStatus.NOTFOUND]:
            LOADING_STYLE["display"] = "none"
            return 0, LOADING_STYLE, job.dict()
        else:
            if state == -1:
                return no_update
            LOADING_STYLE["display"] = "block"
            return -1, LOADING_STYLE, no_update