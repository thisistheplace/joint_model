import gmsh

from app.interfaces.model import Tubular

from .specs import MeshSpecs
from ...interfaces.geometry import *

FACTORY = gmsh.model.occ


def create_ring(tube: Tubular) -> int:
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
    disk = FACTORY.addDisk(origin.x, origin.y, origin.z)

    return FACTORY.addWire()


def add_cylinder(tube: Tubular) -> int:
    """Returns int tag of created cylinder geometry"""
    return FACTORY.addCylinder(
        tube.axis.point.x,
        tube.axis.point.y,
        tube.axis.point.z,
        tube.axis.vector.x,
        tube.axis.vector.y,
        tube.axis.vector.z,
        tube.diameter / 2.0,
    )
