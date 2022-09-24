import math
import numpy as np
import pytest
import sympy
import sys

sys.path.append("src")

from app.modelling.geometry.weld import get_weld_intersect_points
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
            axis=Axis3D(point=Point3D(x=0.5, y=0, z=0), vector=Vector3D(x=4, y=0, z=0)),
            diameter=1.,
        )
    )


@pytest.fixture
def circle(master):
    return sympy.Circle(master.axis.point.array[:2], master.diameter / 2.0)


class TestIntersections:
    def test_simple_weld(self, master: NpTubular, slave: NpTubular):
        radius = slave.diameter / 2.
        z = slave.axis.point.array[2]
        expected = [
            np.array([radius, 0., z]),
            np.array([0., radius, z]),
            np.array([-1 * radius, 0., z]),
            np.array([0., -1 * radius, z])
        ]
        got = list(get_weld_intersect_points(master, slave))
        print(expected)
        print(got)
        assert expected == got