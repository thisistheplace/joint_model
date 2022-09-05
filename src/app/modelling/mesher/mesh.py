from collections import defaultdict
from contextlib import contextmanager
import gmsh

from .cylinder import add_cylinder

from ...interfaces.geometry import *
from ...interfaces.model import *


def mesh_tubular(tube: Tubular) -> int:
    """Adds tubular geometry and returns tag id"""
    return add_cylinder(tube)


def mesh_joint(joint: Joint) -> dict[str, int]:
    return {tube.name: mesh_tubular(tube) for tube in joint.tubes}


@contextmanager
def mesh_model(joint: Joint) -> gmsh.model.mesh:
    try:
        gmsh.initialize()

        mesh_joint(joint)

        gmsh.model.occ.synchronize()
        gmsh.option.setNumber("Mesh.MeshSizeMax", 0.1)
        gmsh.model.mesh.generate(3)

        # Gmsh can also identify unique edges and faces (a single edge or face whatever
        # the ordering of their nodes) and assign them a unique tag. This identification
        # can be done internally by Gmsh (e.g. when generating keys for basis
        # functions), or requested explicitly as follows:
        gmsh.model.mesh.createEdges()
        gmsh.model.mesh.createFaces()

        yield gmsh.model.mesh
    finally:
        gmsh.finalize()
