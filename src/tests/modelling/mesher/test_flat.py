from types import NoneType
import gmsh
import pytest
import sys

sys.path.append("src")

from app.modelling.mesher.flat import add_flat_tube
from app.interfaces.examples.joints import EXAMPLE_MODELS
from app.interfaces import *


@pytest.fixture
def tube():
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
class TestAddFlatTube:
    def test_add_flat_tube(self, tube: Model, mesh_specs: MeshSpecs):
        add_flat_tube(tube.joint.master, tube.joint.slaves, mesh_specs)
