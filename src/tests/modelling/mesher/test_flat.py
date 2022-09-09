from collections import deque
from types import NoneType
import gmsh
import numpy as np
import pytest
import sys

sys.path.append("/src")

from app.modelling.mesher.flat import line_points, add_flat_tube
from app.interfaces.examples.joints import EXAMPLE_MODELS
from app.interfaces.mesh import MeshSpecs


@pytest.fixture
def square():
    pnt1 = [0, 0, 0]
    pnt2 = [10, 0, 0]
    pnt3 = [10, 10, 0]
    pnt4 = [0, 10, 0]
    pnts = [pnt1, pnt2, pnt3, pnt4]
    return [np.array(pnt) for pnt in pnts]

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


class TestLinePoints:
    @staticmethod
    def check_loop(points: deque[np.ndarray]):
        points = list(points)
        assert len(points) == 41
        assert np.array_equal(points[0], points[-1])

    @staticmethod
    def check_separation(points: deque[np.ndarray]):
        points = list(points)
        previous = points[0]
        for pnt in points[1:]:
            assert np.linalg.norm(pnt - previous) == 1.0
            previous = pnt

    def test_mesh_square_interval(self, square):
        pnts = line_points(square, interval=10)
        self.check_loop(pnts)
        self.check_separation(pnts)

    def test_mesh_square_size(self, square):
        pnts = line_points(square, size=1)
        self.check_loop(pnts)
        self.check_separation(pnts)

    def test_mesh_square_no_loop(self, square):
        pnts = line_points(square, size=1, loop=False)
        assert not np.array_equal(pnts[0], pnts[-1])
        self.check_separation(pnts)

    def test_no_size_or_interval_error(self, square):
        with pytest.raises(ValueError):
            line_points(square)

    def test_size_and_interval_error(self, square):
        with pytest.raises(ValueError):
            line_points(square, interval=10, size=1)

    def test_too_few_points(self, square):
        with pytest.raises(ValueError):
            line_points([square[0]], interval=10)


@pytest.mark.usefixtures("mesh_context")
class TestAddFlatTube:

    def test_add_flat_tube(self, tube, mesh_specs):
        add_flat_tube(tube, mesh_specs)