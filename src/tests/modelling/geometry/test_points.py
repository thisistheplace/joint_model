from calendar import c
import math
from tabnanny import check
import numpy as np
import pytest
import sympy
import sys

sys.path.append("/src")

from app.modelling.geometry.points import (
    ellipse_segment_angle,
    line_points,
    GeometryException,
    check_ellipse_intersect,
    rotate_points,
    ellipse_points,
    ellipse_quadrant_points
)


@pytest.fixture
def square():
    pnt1 = [0, 0, 0]
    pnt2 = [10, 0, 0]
    pnt3 = [10, 10, 0]
    pnt4 = [0, 10, 0]
    pnts = [pnt1, pnt2, pnt3, pnt4]
    return [np.array(pnt) for pnt in pnts]


@pytest.fixture
def circle():
    return sympy.Ellipse(center=np.array([0.0, 0.0]), hradius=1.0, vradius=1.0)

@pytest.fixture
def offset_circle():
    return sympy.Ellipse(center=np.array([1.0, 0.0]), hradius=1.0, vradius=1.0)

@pytest.fixture
def ellipse():
    return sympy.Ellipse(center=np.array([0.0, 0.0]), hradius=1.0, vradius=2.0)


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


class TestEllipseSegmentAngle:
    def test_ellipse_point_intersect_true(self, circle):
        point = sympy.Point2D([1, 0])
        assert check_ellipse_intersect(circle, point)

    def test_ellipse_point_intersect_false(self, circle):
        point = sympy.Point2D([2, 0])
        assert not check_ellipse_intersect(circle, point)

    def test_ellipse_segment_angle_circle(self, circle):
        tol = 1e-6
        start = sympy.Point2D([1.0, 0.0])
        angle = ellipse_segment_angle(circle, start, 0.0, math.sqrt(2.0), tol)
        assert abs(angle - math.pi / 2) <= tol

    @pytest.mark.skip("Skipped since generated points don't intersect ellipse")
    def test_ellipse_segment_angle_circle_start_not_on_circumference(self, ellipse):
        tol = 1e-6
        start = sympy.Point2D([2.0, 0.0])
        with pytest.raises(GeometryException):
            ellipse_segment_angle(ellipse, start, 0.0, math.sqrt(2.0), tol)

    def test_ellipse_segment_angle_ellipse(self, ellipse):
        tol = 1e-6
        start = sympy.Point2D([1.0, 0.0])
        angle = ellipse_segment_angle(
            ellipse, start, 0.0, math.sqrt(5.0), tol
        )
        assert abs(angle - math.pi / 2) <= tol


class TestEllipsePoint:
    @pytest.mark.skip("Skipped since long running")
    def test_ellipse_quad_on_circle(self, circle: sympy.Ellipse):
        size = 0.05
        points = list(
            ellipse_quadrant_points(
                circle.center,
                radius_x=circle.hradius,
                radius_y=circle.vradius,
                size=size,
                rtol=1e-6,
            )
        )
        assert len(points) == math.ceil(circle.circumference.evalf() / size / 4)

    @pytest.mark.skip("Skipped since long running")
    def test_ellipse_quad_offset_circle(self, offset_circle: sympy.Ellipse):
        size = 0.05
        points = list(
            ellipse_quadrant_points(
                offset_circle.center,
                radius_x=offset_circle.hradius,
                radius_y=offset_circle.vradius,
                size=size,
                rtol=1e-6,
            )
        )
        assert len(points) == math.ceil(offset_circle.circumference.evalf() / size / 4)


class TestRotatePoints:
    def test_rotate_points(self):
        points = np.array([[1.0, 0.0], [0.0, 1.0]])
        expected = np.array([[0.0, 1.0], [-1.0, 0.0]])
        rotated = rotate_points(points, math.pi / 2.0)
        assert np.allclose(expected, rotated)
