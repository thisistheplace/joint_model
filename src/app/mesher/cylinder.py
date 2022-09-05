import gmsh

from app.interfaces.model import Tubular

from .specs import MeshSpecs
from ..interfaces.geometry import *

def create_ring(specs: MeshSpecs, tube: Tubular) -> int:

    return gmsh.model.occ.addWire(
        
    )

def add_cylinder(tube: Tubular) -> int:
    """Returns int tag of created cylinder geometry"""
    return gmsh.model.occ.addCylinder(
        tube.axis.point.x,
        tube.axis.point.y,
        tube.axis.point.z,
        tube.axis.vector.x,
        tube.axis.vector.y,
        tube.axis.vector.z,
        tube.diameter / 2.0
    )