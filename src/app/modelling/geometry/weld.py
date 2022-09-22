from copy import deepcopy
import math
from math import cos, sin, sqrt
import sympy
from typing import Generator

from .vectors import rotate, unit_perp_vector, unit_vector
from .intersections import plane_intersect, flat_tube_intersect, arc_angle_signed
from ...interfaces import *

# TODO: look into https://mathcurve.com/courbes2d.gb/alain/alain.shtml

def get_weld_intersect_points(
    master: NpTubular, slave: NpTubular
) -> Generator[np.ndarray, np.ndarray, None]:
    """X/Z plane"""
    perp = unit_perp_vector(slave.axis.vector.array) * slave.diameter / 2.
    intersect = flat_tube_intersect(master, slave)
    # Radius point is on Y axis at radius
    radius_point = np.array([0., master.diameter / 2.0, intersect[2]])
    # Create X/Z plane at radius point
    p2 = deepcopy(radius_point)
    p2[0] += 1.0
    p3 = deepcopy(radius_point)
    p3[2] += 1.0
    plane: sympy.Plane = sympy.Plane(
        sympy.Point3D(radius_point), sympy.Point3D(p2), sympy.Point3D(p3)
    )

    # Adjust slave vector angle by arc angle (rotate about Z axis)
    circle = sympy.Circle(master.axis.point.array[:2], master.diameter / 2.0)
    arc_angle = arc_angle_signed(circle, radius_point)
    slave_vector = unit_vector(rotate(slave.axis.vector.array, np.array([0.0, 0.0, 1.0]), arc_angle))

    def calc_angle(angle):
        # calculate new vector and point
        rotated_point = radius_point + rotate(perp, slave_vector, angle)
        intersect3D = plane_intersect(slave_vector, rotated_point, plane)
        intersect = np.array(intersect3D, dtype=float)
        print(angle, intersect)
        return intersect

    for degrees in range(0, 361, 10):
        angle = degrees * math.pi / 180.
        if abs(degrees - 360) < 1e-8 or degrees > 360:
            continue
        yield calc_angle(angle)

    return calc_angle(0.0)
