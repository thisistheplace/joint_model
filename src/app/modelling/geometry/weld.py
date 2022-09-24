from copy import deepcopy
import math
from math import cos, sin, sqrt
import sympy
from typing import Generator

from .vectors import rotate, unit_perp_vector, unit_vector
from .intersections import flat_tube_intersect, plane_intersect, intersections, arc_angle_signed
from ...interfaces import *

# TODO: look into https://mathcurve.com/courbes2d.gb/alain/alain.shtml

def get_weld_intersect_points(
    master: NpTubular, slave: NpTubular
) -> Generator[np.ndarray, np.ndarray, None]:
    """X/Z plane"""
    intersect = flat_tube_intersect(master, slave)
    print(intersect)
    # Radius point is on X axis at radius
    radius_point = np.array([master.diameter / 2.0, 0., intersect[2]])
    print(radius_point)
    # Create X/Z plane at radius point
    p2 = deepcopy(radius_point)
    p2[0] += 1.0
    p3 = deepcopy(radius_point)
    p3[2] += 1.0
    plane: sympy.Plane = sympy.Plane(
        sympy.Point3D(radius_point), sympy.Point3D(p2), sympy.Point3D(p3)
    )
    print(plane)
    # Adjust slave vector angle by arc angle (rotate about Z axis)
    circle = sympy.Circle(master.axis.point.array[:2], master.diameter / 2.0)
    print(circle)
    radius_arc_angle = arc_angle_signed(circle, radius_point)
    print(radius_arc_angle)
    intersect_arc_angle = arc_angle_signed(circle, intersect)
    print(intersect_arc_angle)
    arc_angle = radius_arc_angle + intersect_arc_angle
    print(arc_angle)
    slave_vector = rotate(unit_vector(slave.axis.vector.array), np.array([0.0, 0.0, 1.0]), arc_angle)
    print(slave_vector)
    perp = unit_perp_vector(slave_vector) * slave.diameter / 2.
    print(perp)

    def calc_angle(angle):
        # calculate new vector and point
        rotated_point = intersect + rotate(perp, slave_vector, angle)
        pnt_intersect = plane_intersect(slave_vector, rotated_point, plane)
        pnt_intersect = np.array(pnt_intersect, dtype=float)
        return pnt_intersect

    for degrees in range(0, 361, 90):
        angle = degrees * math.pi / 180.
        if abs(degrees - 360) < 1e-8 or degrees > 360:
            continue
        yield calc_angle(angle)

    return calc_angle(0.0)
