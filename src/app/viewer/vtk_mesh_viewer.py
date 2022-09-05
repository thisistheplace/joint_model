from dash import Output, Input, State, html, dcc, callback, MATCH, no_update

import dash_vtk

import dash_bootstrap_components as dbc

import asyncio
import json
import time
import uuid

from .requests import get_mesh
from .gmsh_to_dash import vtk_to_dash


def make_toast(id: str):
    return dbc.Toast(
        id=id,
        header="Model load error",
        is_open=False,
        dismissable=True,
        icon="danger",
        duration=3000,
        # top: 66 positions the toast below the navbar
        style={"position": "fixed", "top": 66, "right": 10, "width": 350, "zIndex": 1000},
    )


class VtkMeshViewerAIO(html.Div):
    # A set of functions that create pattern-matching callbacks of the subcomponents
    class ids:
        dropdown = lambda aio_id: {
            "component": "VtkMeshViewerAIO",
            "subcomponent": "dropdown",
            "aio_id": aio_id,
        }
        vtk = lambda aio_id: {
            "component": "VtkMeshViewerAIO",
            "subcomponent": "vtk",
            "aio_id": aio_id,
        }
        toast = lambda aio_id: {
            "component": "VtkMeshViewerAIO",
            "subcomponent": "toast",
            "aio_id": aio_id,
        }
        loading = lambda aio_id: {
            "component": "VtkMeshViewerAIO",
            "subcomponent": "loading",
            "aio_id": aio_id,
        }
        store = lambda aio_id: {
            "component": "VtkMeshViewerAIO",
            "subcomponent": "store",
            "aio_id": aio_id,
        }
        interval = lambda aio_id: {
            "component": "VtkMeshViewerAIO",
            "subcomponent": "interval",
            "aio_id": aio_id,
        }

    # Make the ids class a public class
    ids = ids

    # Define the arguments of the All-in-One component
    def __init__(self, options: list[str], aio_id: str | None = None):
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
            [  # Equivalent to `html.Div([...])`
                dcc.Dropdown(options, id=self.ids.dropdown(aio_id)),
                dcc.Interval(id=self.ids.interval(aio_id), interval=500, max_intervals=0),
                make_toast(id=self.ids.toast(aio_id)),
                dcc.Store(id=self.ids.store(aio_id)),
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
                                # interactorSettings=[...],       # Binding of mouse events to camera action (Rotate, Pan, Zoom...)
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
        Output(ids.store(MATCH), "data"),
        Output(ids.toast(MATCH), "is_open"),
        Output(ids.toast(MATCH), "children"),
        Input(ids.dropdown(MATCH), "value"),
        prevent_initial_callback=True,
    )
    def update_markdown_style(option):
        if option is None:
            return no_update
        try:
            json_bytes = asyncio.run(get_mesh(option))
            json_data = json.loads(json_bytes.decode("utf-8"))
            return (
                dash_vtk.GeometryRepresentation(
                    [dash_vtk.GeometryRepresentation(vtk_to_dash(json_data))]
                ),
                option,
                no_update,
                no_update,
            )
        except Exception as e:
            return no_update, no_update, True, str(e)

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
        Input(ids.dropdown(MATCH), "value"),
        State(ids.store(MATCH), "data"),
        prevent_initial_call=True,
    )
    def check_loader(new_selection, old_selection):
        if new_selection == old_selection:
            return 0
        else:
            return -1
