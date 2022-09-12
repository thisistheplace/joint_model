import numpy as np
import pytest
import sys

sys.path.append("/src")

from app.modelling.geometry.points import line_points


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
    def check_loop(points: list[np.ndarray]):
        assert len(points) == 41
        assert np.array_equal(points[0], points[-1])

    @staticmethod
    def check_separation(points: list[np.ndarray]):
        previous = points[0]
        for pnt in points[1:]:
            assert np.linalg.norm(pnt - previous) == 1.0
            previous = pnt

    def test_mesh_square_interval(self, square):
        pnts = list(line_points(square, interval=10))
        self.check_loop(pnts)
        self.check_separation(pnts)

    def test_mesh_square_size(self, square):
        pnts = list(line_points(square, size=1))
        self.check_loop(pnts)
        self.check_separation(pnts)

    def test_mesh_square_no_loop(self, square):
        pnts = list(line_points(square, size=1, loop=False))
        assert not np.array_equal(pnts[0], pnts[-1])
        self.check_separation(pnts)

    def test_no_size_or_interval_error(self, square):
        with pytest.raises(ValueError):
            list(line_points(square))

    def test_size_and_interval_error(self, square):
        with pytest.raises(ValueError):
            list(line_points(square, interval=10, size=1))

    def test_too_few_points(self, square):
        with pytest.raises(ValueError):
            list(line_points([square[0]], interval=10))