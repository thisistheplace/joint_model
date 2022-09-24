import sys

sys.path.append("src")

from app.interfaces import *
from app.interfaces.mapper import map_to_np
from app.modelling.mesher.mesh import mesh_model
from app.modelling.geometry.weld import get_weld_intersect_points
from app.converters.mesh import mesh_to_dash_vtk
from app.interfaces.examples.joints import EXAMPLE_MODELS

specs = MeshSpecs(size=0.1)

model = EXAMPLE_MODELS["TJoint"]
# with mesh_model(model, specs) as mesh:
#     dash_data = mesh_to_dash_vtk(mesh)
list(get_weld_intersect_points(map_to_np(model.joint.master), map_to_np(model.joint.slaves[0])))
