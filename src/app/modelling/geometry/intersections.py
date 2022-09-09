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
from turtle import end_fill
import numpy as np
from sympy import Plane, Line3D

from ...interfaces import *

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
    # create tube projection plane
    p1 = master.axis.point.array
    p2 = deepcopy(p1)
    p2[0] += 1.0
    p3 = deepcopy(p1)
    p3[3] += 1.0
    plane = Plane(p1, p2, p3)

    intersects = {} # key: slave.name, value: NpPoint3D of intersection
    for slave in slaves:
        line = Line3D(
            slave.axis.point.array,
            slave.axis.vector.array
        )
        try:
            intersection_plane = plane.intersection(line)
        except Exception as e:
            # Handle some specific exception here where an intersection is not found
            msg = f"Could not find intersection point of tubular {slave.name} with plane of {master.name}.\nEncountered error:\n{e}"
            raise IntersectionError(msg)

        inter_plane_point = np.array(intersection_plane[0], dtype=float)

        # adjust intersection point based on radius of master
        xdistance = inter_plane_point[0] - master.axis.point.array[0]
        if abs(xdistance) > master.diameter / 2.0:
            raise IntersectionError(f"Axis of {slave.name} does not intersect with {master.name}")
        

        
        
        intersects[slave.name] = np.array(intersection[0], dtype=float)
            
    return intersects


def flatten_tube():
    """Flattens """
    pass