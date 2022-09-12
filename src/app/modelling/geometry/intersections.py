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

def intersections(master: NpTubular, slaves: list[NpTubular]) -> list[NpPoint3D]:
    """Calculate 3D points where slaves intersect master
    
    Args:
        master: 3D tubular with slave tubes may intersect
        slaves: list of 3D tubulars which may intersect master

    Returns:
        List of NpPoint3D where slaves intersect with master

    Raises:
        IntersectionError if any of the slaves don't intersect the master

    x = intersection points for KJoint
    plane is tube projection onto flat plane, aligned with tube centreline

        |-----------|
        |           |
        |   x   x   |
        |           |
        |           |
        |   x   x   |
        |           |
        |-----------|
    """
    # TODO: check that slave point doesn't intersect master axis!!!
    intersects = {} # key: slave.name, value: NpPoint3D of intersection
    for slave in slaves:
        # Get 2D point of intersection with the circle
        intersect2D_array = circle_intersect(master, slave)

        # Use point to determine side of circle intersect to use
        for intersect2D in intersect2D_array:
            intersect_vector = intersect2D - master.axis.point.array[:2]
            point_vector = slave.axis.point.array[:2] - master.axis.point.array[:2]
            print(f"intersect {intersect_vector}")
            print(f"point vector {point_vector}")
            angle2D = angle_between_vectors(intersect_vector, point_vector)
            if angle2D <= math.pi / 2:
                break
        print(f"chosen {intersect2D}")

        # create tube projection plane at point of intersect on circle
        # plane is in X/Z system
        p1 = master.axis.point.array
        p1[:2] = intersect2D
        p2 = deepcopy(p1)
        p2[0] += 1.0
        p3 = deepcopy(p1)
        p3[2] += 1.0
        plane: sympy.Plane = sympy.Plane(
            sympy.Point3D(p1),
            sympy.Point3D(p2),
            sympy.Point3D(p3)
        )
        line = get_sympy_line(slave, sympy.Line3D)
        try:
            intersect3D = plane.intersection(line)
        except Exception as e:
            # Handle some specific exception here where an intersection is not found
            msg = f"Could not find intersection point of tubular {slave.name} with plane of {master.name}.\nEncountered error:\n{e}"
            raise IntersectionError(msg)

        intersects[slave.name] = np.array(intersect3D, dtype=float)
            
    return intersects


def circle_intersect(master: NpTubular, slave: NpTubular) -> np.ndarray:
    """Calculate 2D point where slave intersects master tube
    
    https://math.stackexchange.com/questions/311921/get-location-of-vector-circle-intersection

    Args:
        master: 3D tubular with slave tube which may intersect
        slave: 3D tubular which may intersect master

    Returns:
        numpy array where slave intersects with master

    Raises:
        IntersectionError if the slave does not intersect the master
    """
    # Find intersection with circle in 2D plane
    center = sympy.Point2D(
        master.axis.point.array[:2]
    )
    circle = sympy.Circle(
        center,
        master.diameter / 2.0
    )
    line = get_sympy_line(slave, sympy.Line2D)
    try:
        intersect = circle.intersection(line)
        return np.array(intersect, dtype=float)
    except Exception as e:
        # Handle some specific exception here where an intersection is not found
        msg = f"Could not find intersection point of line {line} with circle {circle}.\nEncountered error:\n{e}"
        raise IntersectionError(msg)

def get_sympy_line(tube: NpTubular, line_type: Any) -> sympy.Line:

    if line_type is sympy.Line3D:
        point = tube.axis.point.array
        vector = tube.axis.vector.array

    elif line_type is sympy.Line2D:
        point = tube.axis.point.array[:2]
        vector = tube.axis.vector.array[:2]

    if np.allclose(point, vector):
        vector = vector * 2

    return line_type(point, vector)

def flatten_tube():
    """Flattens """
    pass