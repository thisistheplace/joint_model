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

from app.interfaces.validation import validate_json

from ..ids import Ids
from ..toast import make_toast
from ..vtkmeshviewer import VtkMeshViewerAIO
from ....interfaces import Model
from ....interfaces.examples.joints import EXAMPLE_JOINTS


class VtkFileInputAIO(VtkMeshViewerAIO):

    # Make the ids class a public class
    ids = Ids

    # Define the arguments of the All-in-One component
    def __init__(self, options: list[str]):
        """VtkFileInputAIO is an All-In-One component which passes JSON data to a rest API"""
        aio_id = str(uuid.uuid4())

        # Define the component's layout
        super().__init__(
            aio_id,
            [   
                make_toast(id=self.ids.exampletoast(aio_id), header="Invalid example error"),
                make_toast(id=self.ids.texttoast(aio_id), header="Invalid json input"),
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
                            dcc.Store(id=self.ids.textjsonstore(aio_id)),
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
                                    dbc.AccordionItem(
                                        [
                                            html.Div(
                                                dbc.Button("Upload JSON", id=self.ids.textupload(aio_id), color="success", className="me-1", style={"padding": "10px"}),
                                                style={"paddingTop":"10px", "paddingBottom":"10px"}
                                            ),
                                            # json input
                                            dbc.Textarea(
                                                id=self.ids.textinput(aio_id),
                                                valid=True,
                                                className="mb-3",
                                                placeholder="Paste JSON data here",
                                                style={"height":"100%"}
                                            ),
                                        ],
                                        title="JSON data input"
                                    ),
                                ],
                                style={"paddingTop": "20px"}
                            ),
                        ],
                        style={"height": "100%", "width": "100%", "maxWidth": "100%"},
                    ),
                    id=self.ids.sidepanel(aio_id),
                    is_open=True
                ),
            ],
            options,
        )

    # Define this component's stateless pattern-matching callback
    # that will apply to every instance of this component.
    @callback(
        Output(ids.jsonstore(MATCH), "data"),
        Output(ids.exampletoast(MATCH), "is_open"),
        Output(ids.exampletoast(MATCH), "children"),
        Input(ids.dropdown(MATCH), "value"),
        Input(ids.textjsonstore(MATCH), "data"),
        prevent_initial_call=True,
    )
    def get_example_joint(option, json_data):
        if option is None and json_data is not None:
            return json_data, no_update, no_update
        if option not in EXAMPLE_JOINTS:
            msg = f"Model {option} is not in the available models!"
            return no_update, True, msg
        # create model response
        model = Model(name=option, joint=EXAMPLE_JOINTS[option])
        return model.json(), no_update, no_update

    @callback(
        Output(ids.sidepanel(MATCH), "is_open"),
        Input(ids.open(MATCH), "n_clicks"),
        Input(ids.close(MATCH), "n_clicks"),
        prevent_initial_callback=True,
    )
    def toggle_collapse(n_open, n_close):
        button_id = callback_context.triggered[0]["prop_id"].split(".")[0]
        if button_id == "":
            return no_update
        button_id = literal_eval(button_id)
        if button_id["subcomponent"] == "open":
            return True
        elif button_id["subcomponent"] == "close":
            return False
        else:
            return no_update

    @callback(
        Output(ids.textjsonstore(MATCH), "data"),
        Output(ids.texttoast(MATCH), "is_open"),
        Output(ids.texttoast(MATCH), "children"),
        Input(ids.textupload(MATCH), "n_clicks"),
        State(ids.textinput(MATCH), "value"),
        prevent_initial_callback=True,
    )
    def load_json(n_clicks, json_str):
        # load model data
        if json_str is None:
            return no_update
        elif json_str == "":
            return no_update, True, "Could not load an empty string"
        else:
            try:
                model_data = validate_json(json_str, Model)
                return model_data, no_update, no_update
            except Exception as e:
                return no_update, True, str(e)

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
