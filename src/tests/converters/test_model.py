import pytest
import sys

sys.path.append("/src")


from app.interfaces import *
from app.modelling.mesher.mesh import mesh_model
from app.converters.mesh import mesh_to_dash_vtk
from app.interfaces.examples.joints import EXAMPLE_MODELS

@pytest.fixture
def mesh_specs():
    return MeshSpecs(size=0.1)

class TestMeshToDashVtk:
    def test_mesh_to_dash_vtk_success(self, mesh_specs):
        model = EXAMPLE_MODELS["TJoint"]
        with mesh_model(model, mesh_specs) as mesh:
            dash_data = mesh_to_dash_vtk(mesh)

        assert isinstance(dash_data, DashVtkMesh)
        assert dash_data == DashVtkMesh.parse_obj(dash_data.dict())
