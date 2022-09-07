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

import json
import uuid

from .fileutils import parse_contents
from ..ids import Ids
from ..toast import make_toast
from ..vtkmeshviewer import VtkMeshViewerAIO
from ....interfaces import Model
from ....interfaces.examples.joints import EXAMPLE_JOINTS
from ....interfaces.validation import validate_json


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
                make_toast(
                    id=self.ids.exampletoast(aio_id), header="Invalid example error"
                ),
                make_toast(id=self.ids.texttoast(aio_id), header="Invalid json input"),
                make_toast(id=self.ids.filetoast(aio_id), header="Invalid json file"),
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
                        "padding": "10px",
                    },
                ),
                dbc.Offcanvas(
                    dbc.Container(
                        [
                            dcc.Store(id=self.ids.textjsonstore(aio_id)),
                            dcc.Store(id=self.ids.filejsonstore(aio_id)),
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
                                        title="Mesh example model",
                                    ),
                                    dbc.AccordionItem(
                                        [
                                            dbc.Button(
                                                "Download",
                                                id=self.ids.downloadbutton(aio_id),
                                                className="mb-3",
                                                n_clicks=0,
                                            ),
                                            dcc.Download(
                                                id=self.ids.download(aio_id),
                                            ),
                                        ],
                                        title="Download example model",
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
                                                dbc.Button(
                                                    "Upload JSON",
                                                    id=self.ids.textupload(aio_id),
                                                    color="success",
                                                    className="me-1",
                                                    style={"padding": "10px"},
                                                ),
                                                style={
                                                    "paddingTop": "10px",
                                                    "paddingBottom": "10px",
                                                },
                                            ),
                                            # json input
                                            dbc.Textarea(
                                                id=self.ids.textinput(aio_id),
                                                valid=True,
                                                className="mb-3",
                                                placeholder="Paste JSON data here",
                                                style={"height": "100%"},
                                            ),
                                        ],
                                        title="JSON data input",
                                    ),
                                ],
                                style={"paddingTop": "20px"},
                            ),
                        ],
                        style={"height": "100%", "width": "100%", "maxWidth": "100%"},
                    ),
                    id=self.ids.sidepanel(aio_id),
                    is_open=True,
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
        Input(ids.filejsonstore(MATCH), "data"),
        prevent_initial_call=True,
    )
    def get_example_joint(modelname, text_json, file_json):
        if modelname is None:
            if text_json is not None:
                return text_json, no_update, no_update
            if file_json is not None:
                return file_json, no_update, no_update
        if modelname not in EXAMPLE_JOINTS:
            msg = f"Model {modelname} is not in the available models!"
            return no_update, True, msg
        # create model response
        model = Model(name=modelname, joint=EXAMPLE_JOINTS[modelname])
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
        button_id = json.loads(button_id)
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

    @callback(
        Output(ids.filejsonstore(MATCH), "data"),
        Output(ids.filetoast(MATCH), "is_open"),
        Output(ids.filetoast(MATCH), "children"),
        Input(ids.fileupload(MATCH), "contents"),
        State(ids.fileupload(MATCH), "filename"),
        prevent_initial_call=True,
    )
    def load_file(file_contents, filename):
        try:
            json_data = parse_contents(file_contents, filename)
            return json_data, False, no_update
        except Exception as e:
            return no_update, True, str(e)

    @callback(
    Output(ids.download(MATCH), "data"),
    Input(ids.downloadbutton(MATCH), "n_clicks"),
    State(ids.dropdown(MATCH), "value"),
    prevent_initial_call=True,
    )
    def func(n_clicks, modelname):
        if modelname not in EXAMPLE_JOINTS.keys():
            modelname = list(EXAMPLE_JOINTS.keys())[-1]
        modelobj = Model(
            name = modelname,
            joint = EXAMPLE_JOINTS[modelname]
        )
        modeldata = json.loads(modelobj.json())
        return dcc.send_string(json.dumps(modeldata, indent=4), f"{modelname}.json")