import math
import numpy as np
import pytest
import sys

sys.path.append("/src")

from app.modelling.geometry.intersections import intersections
from app.interfaces import *
from app.interfaces.mapper import map_to_np


@pytest.fixture
def master():
    return map_to_np(
        Tubular(
            name="master",
            axis=Axis3D(point=Point3D(x=0, y=0, z=-2), vector=Vector3D(x=0, y=0, z=4)),
            diameter=2.0,
        )
    )


@pytest.fixture
def slave():
    return map_to_np(
        Tubular(
            name="slave",
            axis=Axis3D(point=Point3D(x=0, y=1, z=0), vector=Vector3D(x=0, y=4, z=0)),
            diameter=1,
        )
    )


class TestIntersections:
    """
            |
    quad 4  |   quad 3
            |
    X-----------------
            |
    quad 1  |   quad 2
            |
            Y
    """

    def test_align_point_with_pos_y(self, master: NpTubular, slave: NpTubular):
        point = intersections(master, slave)
        assert np.allclose(point, np.array([0, 1, 0]))

    def test_align_point_with_neg_y(self, master: NpTubular, slave: NpTubular):
        slave.axis.point.array[1] = -1
        point = intersections(master, slave)
        assert np.allclose(point, np.array([0, -1, 0]))

    def test_quad_1(self, master: NpTubular, slave: NpTubular):
        slave.axis.point.array = np.array([1, 1, 0])
        slave.axis.vector.array = np.array([1, 1, 0])
        point = intersections(master, slave)
        assert np.allclose(
            point,
            np.array([math.cos(math.pi / 4), math.cos(math.pi / 4), 0])
        )

    def test_quad_2(self, master: NpTubular, slave: NpTubular):
        slave.axis.point.array = np.array([-1, 1, 0])
        slave.axis.vector.array = np.array([-1, 1, 0])
        point = intersections(master, slave)
        assert np.allclose(
            point,
            np.array([-1 * math.cos(math.pi / 4), math.cos(math.pi / 4), 0]),
        )

    def test_quad_3(self, master: NpTubular, slave: NpTubular):
        slave.axis.point.array = np.array([-1, -1, 0])
        slave.axis.vector.array = np.array([-1, -1, 0])
        point = intersections(master, slave)
        assert np.allclose(
            point,
            np.array([-1 * math.cos(math.pi / 4), -1 * math.cos(math.pi / 4), 0]),
        )

    def test_quad_4(self, master: NpTubular, slave: NpTubular):
        slave.axis.point.array = np.array([1, -1, 0])
        slave.axis.vector.array = np.array([1, -1, 0])
        point = intersections(master, slave)
        assert np.allclose(
            point,
            np.array([math.cos(math.pi / 4), -1 * math.cos(math.pi / 4), 0]),
        )

    def test_quad_1_zshift(self, master: NpTubular, slave: NpTubular):
        slave.axis.point.array = np.array([1, 1, 4])
        slave.axis.vector.array = np.array([1, 1, 4])
        point = intersections(master, slave)
        assert np.allclose(
            point,
            np.array([math.cos(math.pi / 4), math.cos(math.pi / 4), 4])
        )
