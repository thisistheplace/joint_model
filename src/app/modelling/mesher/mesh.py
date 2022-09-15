from contextlib import contextmanager
import gmsh
from itertools import combinations

from .cylinder import add_cylinder
from .flat import add_flat_tube
from .holes import create_holes

from ...interfaces.geometry import *
from ...interfaces.model import *
from ...interfaces.mesh import *
from ...interfaces.mapper import map_to_np

FACTORY = gmsh.model.occ

# TODO: need to handle memory exceptions!!! Or try and predict memory usage!


def mesh_master(tube: Tubular, specs: MeshSpecs) -> tuple[int, int]:
    """Adds tubular geometry and returns tag id"""
    return add_cylinder(tube)
    # return add_flat_tube(tube, specs)

def mesh_slaves(tube: Tubular, specs: MeshSpecs) -> tuple[int, int]:
    """Adds tubular geometry and returns tag id"""
    return add_cylinder(tube)
    # return add_flat_tube(tube, specs)

def mesh_joint(joint: Joint, specs: MeshSpecs) -> dict[str, tuple[int, int]]:
    joint_mesh = {}
    joint_mesh.update({joint.master.name: mesh_master(joint.master, specs)})
    joint_mesh.update({tube.name: mesh_slaves(tube, specs) for tube in joint.slaves})
    # TODO: move map to decorator?
    specs = MeshSpecs(size=0.01)
    #create_holes(map_to_np(joint.master), [map_to_np(tube) for tube in joint.slaves], specs)
    FACTORY.synchronize()
    for k, (dim, mesh) in joint_mesh.items():
        gid = gmsh.model.addPhysicalGroup(dim, [mesh])
        gmsh.model.setPhysicalName(dim, gid, k)
        return joint_mesh


@contextmanager
def mesh_model(model: Model, specs: MeshSpecs) -> gmsh.model.mesh:
    try:
        gmsh.initialize()
        meshed_tubes = mesh_joint(model.joint, specs)

        FACTORY.synchronize()

        # attempt all intersections
        for comb in combinations(meshed_tubes.values(), 2):
            intersect = FACTORY.intersect(
                [comb[0]], [comb[1]], removeObject=False, removeTool=False
            )
            FACTORY.synchronize()
            if len(intersect[0]) > 0:
                # if there is an intersection, do what you want to do.
                FACTORY.remove(
                    intersect[0], True
                )  # remove created intersection objects
                FACTORY.synchronize()
            else:
                pass
                # raise Exception("SHOULD BE AN INTERSECTION")

        FACTORY.synchronize()
        gmsh.option.setNumber("Mesh.MeshSizeMax", 0.05)
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
