from cmath import exp
import math
import numpy as np
import sys

sys.path.append("src")

from app.modelling.geometry.vectors import rotate


class TestRotate:
    def test_rotate_90(self):
        point = np.array([1.0, 0.0, 0.0])
        axis = np.array(
            [
                0.0,
                0.0,
                1,
            ]
        )
        angle = math.pi / 2.0
        expected = np.array([0.0, 1.0, 0.0])
        got = rotate(point, axis, angle)
        assert np.allclose(got, expected)
