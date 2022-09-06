from dash import Output, Input, State, html, dcc, callback, MATCH, no_update
import dash_vtk

import asyncio
import time
import uuid

from ..ids import Ids
from ..toast import make_toast
from ...gmsh_to_dash import vtk_to_dash
from ...requests.exceptions import MeshApiHttpError
from ...requests.requests import get_mesh
from ....interfaces import Model
from ....interfaces.validation import validate_json


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
                    id=self.ids.interval(aio_id), interval=500, max_intervals=0
                ),
                make_toast(id=self.ids.requesttoast(aio_id), header="Model load error"),
                dcc.Store(id=self.ids.jsonstore(aio_id)),
                dcc.Loading(
                    id=self.ids.loading(aio_id),
                    children=[
                        html.Div(
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
                            style={"height": "100vh", "width": "100vw"},
                        )
                    ],
                    type="circle",
                ),
            ],
            style={"height": "100vh", "width": "100vw"},
        )

    # Define this component's stateless pattern-matching callback
    # that will apply to every instance of this component.
    @callback(
        Output(ids.vtk(MATCH), "children"),
        Output(ids.requesttoast(MATCH), "is_open"),
        Output(ids.requesttoast(MATCH), "children"),
        Input(ids.jsonstore(MATCH), "data"),
        prevent_initial_callback=True,
    )
    def update_markdown_style(json_str: str):
        if json_str is None:
            return no_update
        try:
            json_model = validate_json(json_str, Model)
            json_mesh = asyncio.run(get_mesh(json_model))
            return (
                dash_vtk.GeometryRepresentation(
                    [dash_vtk.GeometryRepresentation(vtk_to_dash(json_mesh))]
                ),
                no_update,
                no_update,
            )
        except MeshApiHttpError as e:
            return no_update, True, e.toast_message
        except Exception as e:
            return no_update, True, str(e)

    @callback(
        Output(ids.interval(MATCH), "interval"),
        Input(ids.interval(MATCH), "n_intervals"),
        prevent_initial_call=True,
    )
    def model_loading_wheel(n):
        time.sleep(0.5)
        return no_update

    @callback(
        Output(ids.interval(MATCH), "max_intervals"),
        Input(ids.jsonstore(MATCH), "data"),
        State(ids.jsonstore(MATCH), "data"),
        prevent_initial_call=True,
    )
    def check_loader(new_selection, old_selection):
        if new_selection == old_selection:
            return 0
        else:
            return -1
