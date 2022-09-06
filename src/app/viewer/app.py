"""This is currently just for aiding development / testing"""
from dash import Dash
import dash_bootstrap_components as dbc

from .models import DEMO_MODELS
from .layout.layout import VtkFileInputAIO

# Dash setup
app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY, dbc.icons.FONT_AWESOME])
server = app.server

app.layout = VtkFileInputAIO(options=list(DEMO_MODELS.keys()))
