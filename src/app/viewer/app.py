"""This is currently just for aiding development / testing"""
from dash import Dash

from .models import DEMO_MODELS
from .vtk_mesh_viewer import VtkMeshViewerAIO

# Dash setup
app = Dash(__name__)
server = app.server

app.layout = VtkMeshViewerAIO(list(DEMO_MODELS.keys()))