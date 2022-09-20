import sys

sys.path.append("/src")

from app.interfaces import *
from app.modelling.mesher.mesh import mesh_model
from app.converters.mesh import mesh_to_dash_vtk
from app.interfaces.examples.joints import EXAMPLE_MODELS

specs = MeshSpecs(size=0.1)

model = EXAMPLE_MODELS["TJoint"]
with mesh_model(model, specs) as mesh:
    dash_data = mesh_to_dash_vtk(mesh)