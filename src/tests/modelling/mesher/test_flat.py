from types import NoneType
import gmsh
import pytest
import sys

sys.path.append("/src")

from app.modelling.mesher.flat import add_flat_tube
from app.interfaces.examples.joints import EXAMPLE_MODELS
from app.interfaces.mesh import MeshSpecs


@pytest.fixture
def tube():
    return EXAMPLE_MODELS["TJoint"].joint.tubes[0]

@pytest.fixture
def mesh_specs():
    return MeshSpecs(
        size=0.1
    )

@pytest.fixture
def mesh_context() -> NoneType:
    try:
        gmsh.initialize()
        yield
    finally:
        gmsh.finalize()


@pytest.mark.usefixtures("mesh_context")
class TestAddFlatTube:

    def test_add_flat_tube(self, tube, mesh_specs):
        add_flat_tube(tube, mesh_specs)