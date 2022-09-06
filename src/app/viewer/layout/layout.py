from dash import (
    Output,
    Input,
    State,
    html,
    dcc,
    callback,
    MATCH,
    no_update,
    callback_context,
)
import dash_bootstrap_components as dbc

from ast import literal_eval
import uuid

from .vtk import VtkMeshViewerAIO


class VtkFileInputAIO(VtkMeshViewerAIO):
    # A set of functions that create pattern-matching callbacks of the subcomponents
    # Extend for components added by the layout
    class ids(VtkMeshViewerAIO.ids):
        dropdown = lambda aio_id: {
            "component": "VtkMeshViewerAIO",
            "subcomponent": "dropdown",
            "aio_id": aio_id,
        }
        freeinput = lambda aio_id: {
            "component": "VtkFileInputAIO",
            "subcomponent": "freeinput",
            "aio_id": aio_id,
        }
        fileupload = lambda aio_id: {
            "component": "VtkFileInputAIO",
            "subcomponent": "fileupload",
            "aio_id": aio_id,
        }
        inputstore = lambda aio_id: {
            "component": "VtkFileInputAIO",
            "subcomponent": "inputstore",
            "aio_id": aio_id,
        }
        # Sidepanel stuff
        sidepanel = lambda aio_id: {
            "component": "VtkFileInputAIO",
            "subcomponent": "sidepanel",
            "aio_id": aio_id,
        }
        open = lambda aio_id: {
            "component": "VtkFileInputAIO",
            "subcomponent": "open",
            "aio_id": aio_id,
        }
        close = lambda aio_id: {
            "component": "VtkFileInputAIO",
            "subcomponent": "close",
            "aio_id": aio_id,
        }

    # Make the ids class a public class
    ids = ids

    # Define the arguments of the All-in-One component
    def __init__(self, options: list[str]):
        """VtkFileInputAIO is an All-In-One component which passes JSON data to a rest API"""
        aio_id = str(uuid.uuid4())

        # Define the component's layout
        super().__init__(
            aio_id,
            [   
                html.Div(
                    dbc.Button(
                        html.I(className="fa fa-bars"),
                        id=self.ids.open(aio_id),
                        className="mb-3",
                        n_clicks=0,
                    ),
                    style={
                        "z-index": "1000",
                        "position": "absolute",
                        "display": "block",
                        "padding": "10px"
                    },
                ),
                dbc.Offcanvas(
                    dbc.Container(
                        [
                            dcc.Store(id=self.ids.inputstore(aio_id)),
                            html.Div(
                                dbc.Button(
                                    html.I(className="fa-solid fa-xmark"),
                                    id=self.ids.close(aio_id),
                                    className="mb-3",
                                    n_clicks=0,
                                ),
                                style={
                                    "position": "absolute",
                                    "display": "block",
                                    "top": "0px",
                                    "right": "0px",
                                    "padding": "20px",
                                    "zindex": "1000",
                                },
                            ),
                            dbc.Accordion(
                                [
                                    dbc.AccordionItem(
                                        dcc.Dropdown(
                                            options, id=self.ids.dropdown(aio_id)
                                        ),
                                        title="Select model",
                                    ),
                                    dbc.AccordionItem(
                                        dcc.Upload(
                                            id=self.ids.fileupload(aio_id),
                                            children=html.Div(
                                                [
                                                    "Drag and Drop or ",
                                                    html.A("Select Files"),
                                                ]
                                            ),
                                            style={
                                                "width": "100%",
                                                "height": "60px",
                                                "lineHeight": "60px",
                                                "borderWidth": "1px",
                                                "borderStyle": "dashed",
                                                "borderRadius": "5px",
                                                "textAlign": "center",
                                                "margin": "10px",
                                            },
                                            multiple=False,
                                        ),
                                        title="Upload file",
                                    ),
                                ],
                                style={"paddingTop": "20px"}
                            ),
                        ],
                        style={"height": "100%", "width": "100%", "maxWidth": "100%"},
                    ),
                    id=self.ids.sidepanel(aio_id),
                    is_open=False
                ),
            ],
            options,
        )

    # Define this component's stateless pattern-matching callback
    # that will apply to every instance of this component.
    @callback(
        Output(ids.store(MATCH), "data"),
        Input(ids.dropdown(MATCH), "value"),
        prevent_initial_call=True,
    )
    def check_loader(option):
        return option

    @callback(
        Output(ids.sidepanel(MATCH), "is_open"),
        Input(ids.open(MATCH), "n_clicks"),
        Input(ids.close(MATCH), "n_clicks"),
        prevent_initial_callback=True,
    )
    def toggle_collapse(n_open, n_close):
        button_id = callback_context.triggered[0]["prop_id"].split(".")[0]
        button_id = literal_eval(button_id)
        if button_id["subcomponent"] == "open":
            return True
        elif button_id["subcomponent"] == "close":
            return False
        else:
            return no_update

    # @app.callback(
    #     Output("wheel-interval", "max_intervals"),
    #     Input('upload-data', 'contents'),
    #     Input(self.id, 'ifc_file_contents'),
    #     State("upload-data", "filename"),
    #     State(self.id, 'ifc_file_contents'),
    #     prevent_initial_call=True
    # )
    # def check_loader(file_contents, new_contents, filename, old_data):
    #     if parse_contents(file_contents, filename) == old_data:
    #         return 0
    #     else:
    #         return -1

    # @app.callback(
    #     Output("wheel-interval", "interval"),
    #     Input('wheel-interval', 'n_intervals'),
    #     prevent_initial_call=True
    # )
    # def model_loading_wheel(n):
    #     time.sleep(0.5)
    #     return no_update

    # @app.callback(
    #     Output("user-model-load-error", "is_open"),
    #     Output("user-model-load-error", "children"),
    #     Output(self.id, "ifc_file_contents"),
    #     Input('upload-data', 'contents'),
    #     State('upload-data', 'filename'),
    #     prevent_initial_call=True
    # )
    # def model_to_ifc(file_contents, filename):
    #     try:
    #         ifc_data = parse_contents(file_contents, filename)
    #         return False, no_update, ifc_data
    #     except Exception as e:
    #         return True, f"Failed to load model:\n{e}", no_update

    # @app.callback(
    #     Output("default-model-load-error", "is_open"),
    #     Output("default-model-load-error", "children"),
    #     Output('upload-data', 'contents'),
    #     Output('upload-data', 'filename'),
    #     Output('select-model', 'label'),
    #     Input({'type': 'model-selection', 'index': ALL}, 'n_clicks'),
    #     State({'type': 'model-selection', 'index': ALL}, 'children'),
    #     prevent_initial_call=True
    # )
    # def download_model(n_clicks, labels):
    #     try:
    #         button_info = literal_eval(callback_context.triggered[0]["prop_id"].split(".")[0])
    #         model_name = labels[button_info["index"]]
    #         fname, model = read_model(model_name)
    #         model_bytes = base64.b64encode(bytes(model, 'utf-8'))
    #         return no_update, no_update, f"none,{str(model_bytes, 'utf-8')}", fname, model_name
    #     except Exception as e:
    #         return True, f"Failed to load model:\n{e}", no_update, no_update, no_update
