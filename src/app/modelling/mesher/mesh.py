"""Overall approach of generating a mesh

1. Re-orient into an easy to manage plane
    a. Rotate all tubulars about the master.point such that the master
    vector is aligned with the Z axis

2. Tubular intersections center point
    a. Create XZ plane (master vector is now on this plane)
    b. Calculate the intersections of the slave tubes on the XZ plane
    c. Offset the intersections to the tube surface

3. Tubular intersections weldline
    a. Create XZ plane at each intersection center point
    b. Create ellipse of points on this plane aligned with correct orientation (?)

4. Wrap into tubular
    a. Take planes and wrap them into tubulars

5. Reorientate everything based on inverse of 1.


OR

1. Use vector maths

OR

1. Find intersection at vectors offset from tube centreline
    
"""
from asyncio import constants
from contextlib import contextmanager
import gmsh
from itertools import combinations

from .cylinder import add_cylinder
from .flat import add_flat_tube

from ...interfaces.geometry import *
from ...interfaces.model import *
from ...interfaces.mesh import *
from ...interfaces.mapper import map_to_np

from ..geometry.intersections import intersection

FACTORY = gmsh.model.occ

# TODO: need to handle memory exceptions!!! Or try and predict memory usage!


def mesh_master(
    tube: Tubular, slaves: list[Tubular], specs: MeshSpecs
) -> tuple[int, int]:
    """Adds tubular geometry and returns tag id"""
    # return add_cylinder(tube)
    return add_flat_tube(tube, slaves, specs)


def mesh_slaves(tube: Tubular, specs: MeshSpecs) -> tuple[int, int]:
    """Adds tubular geometry and returns tag id"""
    return add_cylinder(tube)
    # return add_flat_tube(tube, specs)


def mesh_joint(joint: Joint, specs: MeshSpecs) -> dict[str, tuple[int, int]]:
    joint_mesh = {}
    master_surface = mesh_master(joint.master, joint.slaves, specs)
    joint_mesh.update(
        {joint.master.name: master_surface}
    )
    # joint_mesh.update({tube.name: mesh_slaves(tube, specs) for tube in joint.slaves})
    # TODO: move map to decorator?
    FACTORY.synchronize()
    for k, (dim, mesh) in joint_mesh.items():
        gid = gmsh.model.addPhysicalGroup(dim, [mesh])
        gmsh.model.setPhysicalName(dim, gid, k)
    return joint_mesh


@contextmanager
def mesh_model(model: Model, specs: MeshSpecs) -> gmsh.model.mesh:
    try:
        gmsh.initialize()
        # set messaging level to errors
        # gmsh.option.setNumber("General.Verbosity", 1)

        meshed_tubes = mesh_joint(model.joint, specs)

        FACTORY.synchronize()
        
        gmsh.option.setNumber("Mesh.RecombineAll", 1)
        gmsh.option.setNumber("Mesh.RecombinationAlgorithm", 3)

        gmsh.option.setNumber("Mesh.MeshSizeMax", 0.1)
        # gmsh.option.setNumber("Mesh.Smoothing", 100)
        # gmsh.option.setNumber("Mesh.Algorithm", 8)
        gmsh.model.mesh.generate(2)

        # Gmsh can also identify unique edges and faces (a single edge or face whatever
        # the ordering of their nodes) and assign them a unique tag. This identification
        # can be done internally by Gmsh (e.g. when generating keys for basis
        # functions), or requested explicitly as follows:
        gmsh.model.mesh.createEdges()
        gmsh.model.mesh.createFaces()

        yield gmsh.model.mesh
    finally:
        gmsh.finalize()
