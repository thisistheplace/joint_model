from copy import deepcopy
import math
from math import cos, sin, sqrt
import sympy
from typing import Generator

from .vectors import unit_vector, rotate
from .intersections import plane_intersect, flat_tube_intersect, arc_angle_signed
from ...interfaces import *

# TODO: look into https://mathcurve.com/courbes2d.gb/alain/alain.shtml

def x(r1: float, r2: float, pheta: float) -> float:
    return -1 * \
        sqrt(-1 * (r2 ** 2) + (r2 ** 2) * (cos(pheta) ** 2)+ (r1 ** 2))

def y(r2: float, pheta: float) -> float:
    return r2 * sin(pheta)

def z(r1: float, r2: float, phi: float, pheta: float) -> float:
    return -1 * \
        (r2 * cos(pheta) - cos(phi) * sqrt(-1 * (r2 ** 2) + (r2 ** 2) * (cos(pheta) ** 2)+ (r1 ** 2))) / \
            sin(phi)

def unit_perp_vector(vector: np.ndarray) -> np.ndarray:
    if vector[1] != 0.0 or vector[2] != 0.0:
        temp = np.array([1., 0., 0.])
    else:
        temp = np.array([0., 1., 0.])
    return unit_vector(np.cross(vector, temp))

def get_weld_intersect_points(master: NpTubular, slave: NpTubular) -> Generator[np.ndarray, np.ndarray, None]:
    """Y/Z plane"""
    perp = unit_perp_vector(slave.axis.vector.array)

    # p2 = deepcopy(master.axis.vector.array)
    # p2[1] += 1.0
    # p3 = deepcopy(master.axis.vector.array)
    # p3[2] += 1.0
    # plane: sympy.Plane = sympy.Plane(
    #     sympy.Point3D(master.axis.vector.array), sympy.Point3D(p2), sympy.Point3D(p3)
    # )

    plane_point = flat_tube_intersect(master, slave)
    # set x coordinate to 0
    plane_point[0] = 0.
    p2 = deepcopy(plane_point)
    p2[1] += 1.0
    p3 = deepcopy(plane_point)
    p3[2] += 1.0
    plane: sympy.Plane = sympy.Plane(
        sympy.Point3D(plane_point), sympy.Point3D(p2), sympy.Point3D(p3)
    )

    # Adjust slave vector angle by arc angle (rotate about Z axis)
    circle = sympy.Circle(master.axis.point.array[:2], master.diameter / 2.0)
    arc_angle = arc_angle_signed(circle, plane_point)
    slave_vector = rotate(slave.axis.vector.array, np.array([0., 0., 1.]), arc_angle)

    for degrees in range(0, 361, 10):
        angle = degrees * math.pi / 180
        # calculate new vector and point
        rotated_point = plane_point + rotate(perp * slave.diameter / 2., slave_vector, angle)
        print(angle, rotated_point)

        # Get 2D point of intersection with the circle
        # intersect2D_array = circle_intersect(master.axis.point.array, master.diameter, rotated_point, rotated_vector)

        # if len(intersect2D_array) == 0:
        #     raise IntersectionError(f"No intersections found for {slave.name} on {master.name} at angle {angle}")

        # # Use point to determine side of circle intersect to use
        # for intersect2D in intersect2D_array:
        #     intersect_vector = intersect2D - master.axis.point.array[:2]
        #     point_vector = rotated_point[:2] - master.axis.point.array[:2]
        #     angle2D = angle_between_vectors(intersect_vector, point_vector)
        #     if angle2D <= math.pi / 2:
        #         break

        # # Determine intersection of vector with plane
        # plane_point = np.array(
        #     [intersect2D[0], intersect2D[1], rotated_point[2]]
        # )
        intersect3D = plane_intersect(slave_vector, rotated_point, plane)
        yield np.array(intersect3D, dtype=float)
