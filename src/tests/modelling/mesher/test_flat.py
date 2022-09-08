from collections import deque
import numpy as np
import pytest
import sys

sys.path.append("/src")

from app.modelling.mesher.flat import line_points


@pytest.fixture
def square():
    pnt1 = [0, 0, 0]
    pnt2 = [10, 0, 0]
    pnt3 = [10, 10, 0]
    pnt4 = [0, 10, 0]
    pnts = [pnt1, pnt2, pnt3, pnt4]
    return [np.array(pnt) for pnt in pnts]


class TestLinePoints:
    @staticmethod
    def validate_points(points: deque[np.ndarray]):
        points = list(points)
        assert len(points) == 41
        assert np.array_equal(points[0], points[-1])
        previous = points[0]
        for pnt in points[1:]:
            assert np.linalg.norm(pnt - previous) == 1.0
            previous = pnt

    def test_mesh_square_interval(self, square):
        self.validate_points(line_points(square, interval=10))

    def test_mesh_square_size(self, square):
        self.validate_points(line_points(square, size=1))