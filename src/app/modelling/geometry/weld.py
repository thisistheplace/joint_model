import math
from math import cos, sin, sqrt

from .vectors import angle_between_vectors
<<<<<<< HEAD
from .intersections import plane_intersect, circle_intersect, IntersectionError
=======
>>>>>>> main
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


<<<<<<< HEAD
def get_weld_intersect_points(master: NpTubular, slave: NpTubular):

    for degrees in range(0, 361, 10):
        angle = degrees * math.pi / 360

        # calculate size of 

        # Get 2D point of intersection with the circle
        intersect2D_array = circle_intersect(master.axis.point.array, master.diameter, slave.axis.point.array, slave.axis.vector.array)

        if len(intersect2D_array) == 0:
            raise IntersectionError(f"No intersections found for {slave.name} on {master.name} at angle {angle}")

        # Use point to determine side of circle intersect to use
        for intersect2D in intersect2D_array:
            intersect_vector = intersect2D - master.axis.point.array[:2]
            point_vector = slave.axis.point.array[:2] - master.axis.point.array[:2]
            angle2D = angle_between_vectors(intersect_vector, point_vector)
            if angle2D <= math.pi / 2:
                break

        # Determine intersection of vector with plane
        plane_point = np.array(
            [intersect2D[0], intersect2D[1], slave.axis.point.array[2]]
        )
        p2 = deepcopy(plane_point)
        p2[0] += 1.0
        p3 = deepcopy(plane_point)
        p3[2] += 1.0
        plane: sympy.Plane = sympy.Plane(
            sympy.Point3D(plane_point), sympy.Point3D(p2), sympy.Point3D(p3)
        )
        intersect3D = plane_intersect(slave.axis.vector.array, plane_point, plane)
        intersects[slave.name] = np.array(intersect3D, dtype=float)
=======
def get_weld_intersect_points():

    for degrees in range(0, 361, 10):
        angle = degrees * math.pi / 360
        
>>>>>>> main
