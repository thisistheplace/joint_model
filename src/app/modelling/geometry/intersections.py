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
from .vectors import angle_between_vectors


class IntersectionError(Exception):
    pass


def intersection(master: NpTubular, slave: NpTubular) -> np.ndarray:
    """Calculate 3D points where slaves intersect master

    Args:
        master: 3D tubular which slave tube may intersect
        slave: 3D tubular which may intersect master

    Returns:
        Dict of np.ndarray where slaves intersect with master (key: NpTubular.name)

    Raises:
        IntersectionError if any of the slaves don't intersect the master
    """
    # TODO: check that slave point doesn't intersect master axis!!!
    # Get 2D point of intersection with the circle
    intersect2D_array = circle_intersect(
        master.axis.point.array,
        master.diameter,
        slave.axis.point.array,
        slave.axis.vector.array,
    )

    if len(intersect2D_array) == 0:
        raise IntersectionError(
            f"No intersections found for {slave.name} on {master.name}"
        )

    # Use point to determine side of circle intersect to use
    for intersect2D in intersect2D_array:
        intersect_vector = intersect2D - master.axis.point.array[:2]
        point_vector = slave.axis.point.array[:2] - master.axis.point.array[:2]
        angle2D = angle_between_vectors(intersect_vector, point_vector)
        if angle2D <= math.pi / 2:
            break

    # Determine intersection of vector with plane
    plane_point = np.array([intersect2D[0], intersect2D[1], slave.axis.point.array[2]])
    p2 = deepcopy(plane_point)
    p3 = deepcopy(plane_point)
    if abs(0.0 - slave.axis.vector.array[0]) < 1e-12:
        p2[0] += 1.0
    else:
        p2[1] += 1.0
    p3[2] += 1.0
    plane: sympy.Plane = sympy.Plane(
        sympy.Point3D(plane_point), sympy.Point3D(p2), sympy.Point3D(p3)
    )
    intersect3D = plane_intersect(slave.axis.vector.array, plane_point, plane)

    return intersect3D


def circle_intersect(
    center: np.ndarray, diameter: float, point: np.ndarray, vector: np.ndarray
) -> np.ndarray:
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

    return line_type(point, point + vector, evaluate=False)


def flat_tube_intersection(master: NpTubular, slave: NpTubular) -> np.ndarray:
    """Get the intersection points of slaves on master if master was unfurled to a plane

    Assumes circle can be constructed from X/Y coordinates. Plane is X/Z. Midpoint of tube
    is aligned with Y axis (X local 2D circle axis).

    Args:
        master: 3D tubular which slave tube may intersect
        slaves: 3D tubular which may intersect master

    Returns:
        Dict of (point: np.ndarray) where point is coordinate slaves
        intersect with master if tube is flattened (key: NpTubular.name)

    Raises:
        IntersectionError if any of the slaves don't intersect the master
    """
    # Get intersections on master surface
    point = intersection(master, slave)
    master_circle = sympy.Circle(master.axis.point.array[:2], master.diameter / 2.0)
    angle = arc_angle_signed(master_circle, point) * -1.0  # -1 since rotation is X to Y
    if angle > math.pi:
        angle = 2 * math.pi - angle
    elif angle < -1 * math.pi:
        angle = -2 * math.pi - angle
    circ_length = (master_circle.circumference / 2.0) * angle / math.pi
    point[0] = circ_length
    # Y coordinate is at tube radius
    point[1] = master.diameter / 2.0
    return point


def arc_angle_signed(circle: sympy.Circle, point: np.ndarray) -> float:
    """Seam (0 rads) is aligned with Y axis

    Positive rotation from X to Y axis (clockwise!)

    Circle is in 2D X/Y plane
    """
    seam = sympy.Point2D(0.0, circle.radius)
    seg_vector = np.empty((3,))
    seg_vector[:2] = point[:2] - np.array(seam.coordinates)
    seg_vector[2] = 0.0
    seg_length = np.linalg.norm(seg_vector)
    sub_angle = math.acos(seg_length / 2.0 / circle.radius)
    return np.sign(circle.center[0] - point[0]) * (math.pi - 2 * sub_angle)


def plane_intersect(
    axis: np.ndarray, point: np.ndarray, plane: sympy.Plane
) -> np.ndarray:
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
    plane_point = np.array(plane.p1, dtype=float)
    plane_normal = np.array(plane.normal_vector, dtype=float)
    epsilon = 1e-6

    try:
        ndotu = plane_normal.dot(axis)
        if abs(ndotu) < epsilon:
            raise IntersectionError(
                f"Cannot compute intersect of vector {axis} which lies in plane {plane}"
            )
        w = point - plane_point
        si = -plane_normal.dot(w) / ndotu
        return w + si * axis + plane_point
    except Exception as e:
        # Handle some specific exception here where an intersection is not found
        msg = f"Could not find intersection point of vector {axis} with plane {plane}.\nEncountered error:\n{e}"
        raise IntersectionError(msg)
