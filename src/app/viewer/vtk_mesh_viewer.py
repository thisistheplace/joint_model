from dash import Output, Input, html, dcc, callback, MATCH, no_update

import dash_vtk
from dash_vtk.utils import to_mesh_state

import dash_bootstrap_components as dbc

import asyncio
import uuid

from .requests import get_vtk_mesh

def make_toast(id:str):
    return dbc.Toast(
        id=id,
        header="Model load error",
        is_open=False,
        dismissable=True,
        icon="danger",
        duration=3000,
        # top: 66 positions the toast below the navbar
        style={"position": "fixed", "top": 66, "right": 10, "width": 350},
    )

class VtkMeshViewerAIO(html.Div):
    # A set of functions that create pattern-matching callbacks of the subcomponents
    class ids:
        dropdown = lambda aio_id: {
            'component': 'VtkMeshViewerAIO',
            'subcomponent': 'dropdown',
            'aio_id': aio_id
        }
        vtk = lambda aio_id: {
            'component': 'VtkMeshViewerAIO',
            'subcomponent': 'vtk',
            'aio_id': aio_id
        }
        toast = lambda aio_id: {
            'component': 'VtkMeshViewerAIO',
            'subcomponent': 'toast',
            'aio_id': aio_id
        }

    # Make the ids class a public class
    ids = ids

    # Define the arguments of the All-in-One component
    def __init__(
        self,
        options: list[str],
        aio_id: str | None = None
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
        super().__init__([  # Equivalent to `html.Div([...])`
            dcc.Dropdown(options, id=self.ids.dropdown(aio_id)),
            make_toast(id=self.ids.toast(aio_id)),
            dash_vtk.View(id=self.ids.vtk(aio_id))
        ],
        style = {
            "height": "100%",
            "width": "100%"
        })

    # Define this component's stateless pattern-matching callback
    # that will apply to every instance of this component.
    @callback(
        Output(ids.vtk(MATCH), 'children'),
        Output(ids.toast(MATCH), 'is_open'),
        Output(ids.toast(MATCH), 'children'),
        Input(ids.dropdown(MATCH), 'value'),
        prevent_initial_callback=True
    )
    def update_markdown_style(option):
        try:
            bytes_content = asyncio.run(get_vtk_mesh(option))
            mesh_state = to_mesh_state(bytes_content)
            return dash_vtk.GeometryRepresentation([
                dash_vtk.Mesh(state=mesh_state)
            ]), no_update, no_update
        except Exception as e:
            return no_update, True, str(e)