"""Unfold a tube and and figure out where intersections are with other tubes

User probably has to define the master tubular which slave tubulars intersect!
E.g. how do you figure out which is the master tube in an X joint?

Process is:
- figure out which tube is main tube
- figure out arc length to intersections
- unfold main tube and intersecting vectors
- calculate shape of intersection of plane and vector / tube (this should be an oval)
- create holes in planar surface
"""
from copy import deepcopy
import math
import numpy as np
import sympy
from typing import Any

from ...interfaces import *
from .vectors import unit_vector, angle_between_vectors


class IntersectionError(Exception):
    pass


def intersections(master: NpTubular, slaves: list[NpTubular]) -> dict[str, np.ndarray]:
    """Calculate 3D points where slaves intersect master

    Args:
        master: 3D tubular with slave tubes may intersect
        slaves: list of 3D tubulars which may intersect master

    Returns:
        Dict of np.ndarray where slaves intersect with master (key: NpTubular.name)

    Raises:
        IntersectionError if any of the slaves don't intersect the master
    """
    # TODO: check that slave point doesn't intersect master axis!!!
    intersects = {}  # key: slave.name, value: NpPoint3D of intersection
    for slave in slaves:
        # Get 2D point of intersection with the circle
        intersect2D_array = circle_intersect(master.axis.point.array, master.diameter, slave.axis.point.array, slave.axis.vector.array)

        if len(intersect2D_array) == 0:
            raise IntersectionError(f"No intersections found for {slave.name} on {master.name}")

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

    return intersects


def plane_intersect(axis: np.ndarray, point: np.ndarray, plane: sympy.Plane) -> np.ndarray:
    """Calculate 3D point where slave intersects plane

    Plane is in X/Z plane.

    Args:
        tube: 3D tubular which may intersect master
        point: 3D numpy array defining a point on the plane

    Returns:
        numpy array where slave intersects with plane

    Raises:
        IntersectionError if the slave does not intersect the master
    """
    # create tube projection plane at point of intersect on circle
    # plane is in X/Z system
    line = get_sympy_line(point, axis, sympy.Line3D)
    try:
        # only one intersect for a line and plane
        intersect = plane.intersection(line)[0]
        if isinstance(intersect, sympy.Line3D):
            return point
        return np.array(intersect, dtype=float)
    except Exception as e:
        # Handle some specific exception here where an intersection is not found
        msg = f"Could not find intersection point of tubular with plane.\nEncountered error:\n{e}"
        raise IntersectionError(msg)


def circle_intersect(center: np.ndarray, diameter: float, point: np.ndarray, vector: np.ndarray) -> np.ndarray:
    """Calculate 2D point where slave intersects master tube

    2D plane is in X/Y plane

    Args:
        master: 3D tubular with slave tube which may intersect
        slave: 3D tubular which may intersect master

    Returns:
        numpy array where slave intersects with master

    Raises:
        IntersectionError if the slave does not intersect the master
    """
    # Find intersection with circle in 2D plane
    center = sympy.Point2D(center[:2])
    circle = sympy.Circle(center, diameter / 2.0)
    line = get_sympy_line(point, vector, sympy.Line2D)
    try:
        intersect = circle.intersection(line)
        return np.array(intersect, dtype=float)
    except Exception as e:
        # Handle some specific exception here where an intersection is not found
        msg = f"Could not find intersection point of line {line} with circle {circle}.\nEncountered error:\n{e}"
        raise IntersectionError(msg)


def get_sympy_line(point: np.ndarray, vector: np.ndarray, line_type: Any) -> sympy.Line:
    """Generate a 2D or 3D sympy line from a point and vector"""
    allowed = [sympy.Line2D, sympy.Line3D]
    if line_type not in allowed:
        raise TypeError(
            f"Cannot generate sympy line type {line_type} since it was not oneof {allowed}."
        )

    if line_type is sympy.Line2D:
        point = point[:2]
        vector = vector[:2]

    if np.allclose(point, vector):
        vector = vector * 2

    return line_type(point, vector)
