import gmsh
import math

from app.interfaces.model import Tubular

from .vectors import angle_between
from ...interfaces.geometry import *

FACTORY = gmsh.model.occ


def rotatexy(dimTags: list[tuple[int, int]], origin: Point3D, vector: Vector3D):
    xangle = angle_between([0, 0, 1], [0, vector.y, vector.z])
    FACTORY.rotate(dimTags, origin.x, origin.y, origin.z, 1, 0, 0, xangle)
    FACTORY.synchronize()

    yangle = angle_between([0, 0, 1], [vector.x, 0, vector.z])
    FACTORY.rotate(dimTags, origin.x, origin.y, origin.z, 0, 1, 0, yangle)
    FACTORY.synchronize()
    print(vector)
    print(xangle, yangle)


def add_tube(tube: Tubular) -> tuple[int, int]:
    origin = tube.axis.point
    vector = tube.axis.vector
    start = FACTORY.addPoint(
        origin.x,
        origin.y,
        origin.z,
    )
    end = FACTORY.addPoint(
        origin.x + vector.x, origin.y + vector.y, origin.z + vector.z
    )
    extrusion = FACTORY.addSpline([start, end])
    wire = FACTORY.addWire([extrusion])

    # Create disk in x, y plane then transform it to be perpendicular
    # to the wire
    radius = tube.diameter / 2.0
    ring = FACTORY.addCircle(origin.x, origin.y, origin.z, radius)
    print(ring)
    rotatexy([(1, ring)], origin, vector)
    pipe = FACTORY.addPipe([(1, ring)], wire)

    # We delete the source surface, and increase the number of sub-edges for a
    # nicer display of the geometry:
    FACTORY.remove([(1, ring)])
    FACTORY.remove([(1, extrusion)])
    gmsh.option.setNumber("Geometry.NumSubEdges", 20)
    return pipe[0]


def add_cylinder(tube: Tubular) -> tuple[int, int]:
    """Returns int tag of created cylinder geometry"""
    pipe = add_tube(tube)
    return pipe
