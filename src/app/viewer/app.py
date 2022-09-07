"""This is currently just for aiding development / testing"""
from dash import Dash
import dash_bootstrap_components as dbc

from ..interfaces.examples.joints import EXAMPLE_MODELS
from .layout import VtkFileInputAIO

# Dash setup
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.FLATLY, dbc.icons.FONT_AWESOME],
    title="JointMesh",
)
server = app.server

app.layout = VtkFileInputAIO(options=list(EXAMPLE_MODELS.keys()))


@app.server.route("/ping")
def ping():
    return "{status: ok}"
