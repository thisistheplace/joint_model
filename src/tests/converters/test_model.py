import sys
from this import d

sys.path.append("/src")

import json

from app.interfaces import *
from app.modelling.mesher.mesh import mesh_model
from app.converters.mesh import mesh_to_dash_vtk
from app.interfaces.examples.joints import EXAMPLE_MODELS


class TestMeshToDashVtk:
    def test_mesh_to_dash_vtk_success(self):
        model = EXAMPLE_MODELS["TJoint"]
        with mesh_model(model) as mesh:
            dash_data = mesh_to_dash_vtk(mesh)

        assert isinstance(dash_data, DashVtkMesh)
        assert dash_data == DashVtkMesh.parse_obj(dash_data.dict())
