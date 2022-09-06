from dash import Output, Input, State, html, dcc, callback, MATCH, no_update
import dash_bootstrap_components as dbc

from typing import Any
import uuid

from .vtk import VtkMeshViewerAIO

class ValidationError(Exception):
    def __init__(self, obj, attr_name):            
        # Call the base class constructor with the parameters it needs
        super().__init__(f"Parent of type {type(obj)} does not have required attribute {attr_name}")

def check_attr(obj, attr_name):
    if not hasattr(obj, attr_name):
        raise ValidationError(obj, attr_name)

def validate_parent(parent: Any):
    to_check = {
        "ids": parent,
        "store": parent.id,
        "vtk": parent.id
    }
    for attr_name, obj in to_check.items():
        check_attr(obj, attr_name)

class VtkFileInputAIO(VtkMeshViewerAIO):
    # A set of functions that create pattern-matching callbacks of the subcomponents
    class ids(VtkMeshViewerAIO.ids):
        freeinput = lambda aio_id: {
            "component": "JsonInputAIO",
            "subcomponent": "freeinput",
            "aio_id": aio_id,
        }
        fileupload = lambda aio_id: {
            "component": "JsonInputAIO",
            "subcomponent": "fileupload",
            "aio_id": aio_id,
        }
        close = lambda aio_id: {
            "component": "JsonInputAIO",
            "subcomponent": "close",
            "aio_id": aio_id,
        }
        inputstore = lambda aio_id: {
            "component": "JsonInputAIO",
            "subcomponent": "inputstore",
            "aio_id": aio_id,
        }

    # Make the ids class a public class
    ids = ids

    # Define the arguments of the All-in-One component
    def __init__(self, parent: Any):
        """VtkFileInputAIO is an All-In-One component which passes JSON data to a rest API

        It is tightly coupled to the parent component.
        """
        if parent is None:
            raise TypeError("parent must not be None!")

        validate_parent(parent)

        if aio_id is None:
            aio_id = str(uuid.uuid4())

        # Define the component's layout
        super().__init__(
            [  # Equivalent to `html.Div([...])`
                dbc.Container(
                    [
                        dcc.Store(id=self.ids.inputstore(aio_id)),
                        html.Div(
                            dbc.Button(
                                html.I(className="fa-solid fa-xmark"),
                                id="sidebar-close",
                                className="mb-3",
                                n_clicks=0,
                                style={"zindex": "10"}
                            ),
                            style={"position":"absolute", "display":"block", "top":"0px", "right":"0px", "padding":"20px"}
                        ),
                        # Heading data
                        html.Div(
                            "In progress...",
                            style={"padding": "30px"}
                        ),
                    ],
                    style={
                        "height": "100%",
                        "width": "100%",
                        "maxWidth":"100%"
                    },
                )
            ],
            style={"height": "100vh", "width": "100vw"},
        )

    # Define this component's stateless pattern-matching callback
    # that will apply to every instance of this component.
    # @callback(
    #     Output(ids.vtk(MATCH), "children"),
    #     Output(ids.store(MATCH), "data"),
    #     Output(ids.toast(MATCH), "is_open"),
    #     Output(ids.toast(MATCH), "children"),
    #     Input(ids.dropdown(MATCH), "value"),
    #     prevent_initial_callback=True,
    # )
    # def update_markdown_style(option):
    #     if option is None:
    #         return no_update
    #     try:
    #         json_bytes = asyncio.run(get_mesh(option))
    #         json_data = json.loads(json_bytes.decode("utf-8"))
    #         return (
    #             dash_vtk.GeometryRepresentation(
    #                 [dash_vtk.GeometryRepresentation(vtk_to_dash(json_data))]
    #             ),
    #             option,
    #             no_update,
    #             no_update,
    #         )
    #     except Exception as e:
    #         return no_update, no_update, True, str(e)