from types import NoneType
import gmsh
import pytest
import sys

sys.path.append("/src")

from app.modelling.mesher.holes import create_holes
from app.interfaces.examples.joints import EXAMPLE_MODELS
from app.interfaces.mapper import map_to_np
from app.interfaces.mesh import MeshSpecs


@pytest.fixture
def joint():
    return EXAMPLE_MODELS["TJoint"].joint


@pytest.fixture
def mesh_specs():
    return MeshSpecs(size=0.01)


@pytest.fixture
def mesh_context() -> NoneType:
    try:
        gmsh.initialize()
        yield
    finally:
        gmsh.finalize()


@pytest.mark.usefixtures("mesh_context")
class TestCreateHoles:
    def test_create_holes(self, joint, mesh_specs):
        master = map_to_np(joint.master)
        slaves = [map_to_np(tube) for tube in joint.slaves]
        holes: dict = create_holes(master, slaves, mesh_specs)
        assert len(list(holes.keys())) == 1
