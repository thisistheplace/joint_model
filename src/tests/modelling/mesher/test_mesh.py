from types import NoneType
import gmsh
import pytest
import sys

sys.path.append("/src")

from app.modelling.mesher.mesh import mesh_joint, mesh_model
from app.interfaces.examples.joints import EXAMPLE_MODELS
from app.interfaces.mesh import MeshSpecs


@pytest.fixture
def joint():
    return EXAMPLE_MODELS["TJoint"].joint


@pytest.fixture
def model():
    return EXAMPLE_MODELS["TJoint"]


@pytest.fixture
def mesh_specs():
    return MeshSpecs(size=0.1)


@pytest.fixture
def mesh_context() -> NoneType:
    try:
        gmsh.initialize()
        yield
    finally:
        gmsh.finalize()


@pytest.mark.usefixtures("mesh_context")
class TestMeshJoint:
    def test_mesh_joint(self, joint, mesh_specs):
        mesh = mesh_joint(joint, mesh_specs)
        assert mesh is not None


class TestMeshModel:
    def test_mesh_model(self, model, mesh_specs):
        with mesh_model(model, mesh_specs) as mesh:
            assert mesh is not None
