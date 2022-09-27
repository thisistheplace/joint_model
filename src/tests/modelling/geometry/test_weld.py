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
def xslave():
    return map_to_np(
        Tubular(
            name="slave",
            axis=Axis3D(
                point=Point3D(x=1.0, y=0.0, z=0), vector=Vector3D(x=4.0, y=0.0, z=0)
            ),
            diameter=1.0,
        )
    )


@pytest.fixture
def xyslave():
    return map_to_np(
        Tubular(
            name="xyslave",
            axis=Axis3D(
                point=Point3D(x=1.0, y=1.0, z=0), vector=Vector3D(x=4.0, y=4.0, z=0)
            ),
            diameter=1.0,
        )
    )


@pytest.fixture
def yslave():
    return map_to_np(
        Tubular(
            name="slave",
            axis=Axis3D(
                point=Point3D(x=0.0, y=1.0, z=0), vector=Vector3D(x=0.0, y=4.0, z=0)
            ),
            diameter=1.0,
        )
    )


class TestIntersections:
    def test_weld_x_axis(self, master: NpTubular, xslave: NpTubular):
        mradius = master.diameter / 2.0
        mcirc = sympy.Circle(master.axis.point.array[:2], mradius)
        xoffset = mcirc.circumference / 4.0
        sradius = xslave.diameter / 2.0
        z = xslave.axis.point.array[2]
        expected = [
            np.array([xoffset - sradius, mradius, z], dtype=float),
            np.array([xoffset, mradius, z + sradius], dtype=float),
            np.array([xoffset + sradius, mradius, z], dtype=float),
            np.array([xoffset, mradius, z - sradius], dtype=float),
        ]
        got = list(get_weld_intersect_points(master, xslave, 90))
        for idx, target in enumerate(expected):
            assert np.allclose(target, got[idx])

    def test_weld_xy45_axis(self, master: NpTubular, xyslave: NpTubular):
        mradius = master.diameter / 2.0
        mcirc = sympy.Circle(master.axis.point.array[:2], mradius)
        xoffset = mcirc.circumference / 4.0 / 2.0
        sradius = xyslave.diameter / 2.0
        z = xyslave.axis.point.array[2]
        expected = [
            np.array([xoffset - sradius, mradius, z], dtype=float),
            np.array([xoffset, mradius, z + sradius], dtype=float),
            np.array([xoffset + sradius, mradius, z], dtype=float),
            np.array([xoffset, mradius, z - sradius], dtype=float),
        ]
        got = list(get_weld_intersect_points(master, xyslave, 90))
        for idx, target in enumerate(expected):
            assert np.allclose(target, got[idx])

    def test_weld_y_axis(self, master: NpTubular, yslave: NpTubular):
        mradius = master.diameter / 2.0
        sradius = yslave.diameter / 2.0
        z = yslave.axis.point.array[2]
        expected = [
            np.array([-1 * sradius, mradius, z]),
            np.array([0.0, mradius, z + sradius]),
            np.array([sradius, mradius, z]),
            np.array([0.0, mradius, z - sradius]),
        ]
        got = list(get_weld_intersect_points(master, yslave, 90))
        for idx, target in enumerate(expected):
            assert np.allclose(target, got[idx])

    def test_angled_y_slave(self, master: NpTubular, yslave: NpTubular):
        yslave.axis.vector.array = np.array([0.0, 1.0, 1.0])
        mradius = master.diameter / 2.0
        sradius = yslave.diameter / 2.0
        z = yslave.axis.point.array[2]
        # output should be ellipse
        expected = [
            np.array([-1 * sradius, mradius, z]),
            np.array([0.0, mradius, z + sradius * math.sqrt(2.0)]),
            np.array([sradius, mradius, z]),
            np.array([0.0, mradius, z - sradius * math.sqrt(2.0)]),
        ]
        got = list(get_weld_intersect_points(master, yslave, 90))
        for idx, target in enumerate(expected):
            assert np.allclose(target, got[idx])
