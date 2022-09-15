from copy import deepcopy
import math
from math import cos, sin, sqrt
from scipy.spatial.transform import Rotation
import sympy
from typing import Generator

from .vectors import angle_between_vectors
from .intersections import plane_intersect, circle_intersect, IntersectionError
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


def get_weld_intersect_points(master: NpTubular, slave: NpTubular) -> Generator[np.ndarray, np.ndarray, None]:
    for degrees in range(0, 361, 10):
        angle = degrees * math.pi / 360

        # calculate new vector and point
        rotation_vector = angle * slave.axis.point.array
        rotation = Rotation.from_rotvec(rotation_vector)
        rotated_point = rotation.apply(slave.axis.point.array)
        rotated_vector = rotation.apply(slave.axis.vector.array)

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
        p2 = deepcopy(rotated_point)
        p2[0] += 1.0
        p3 = deepcopy(rotated_point)
        p3[2] += 1.0
        plane: sympy.Plane = sympy.Plane(
            sympy.Point3D(rotated_point), sympy.Point3D(p2), sympy.Point3D(p3)
        )
        intersect3D = plane_intersect(rotated_vector, rotated_point, plane)
        yield np.array(intersect3D, dtype=float)
