from pygmsh import occ
import meshio

from ..interfaces.geometry import *
from ..interfaces.model import *

def mesh_tubular(geom: occ.Geometry, tube: Tubular) -> occ.geometry.Cylinder:
    return geom.add_cylinder(
        tube.axis.point.dict().values(),
        tube.axis.vector.dict().values(),
        tube.diameter / 2.0
    )

def mesh_joint(geom: occ.Geometry, joint: Joint) -> meshio.Mesh:
    meshed = [mesh_tubular(geom, tube) for tube in joint.tubes]
    geom.boolean_union(meshed)
    mesh = geom.generate_mesh()
    return mesh

def mesh_model(joint: Joint) -> meshio.Mesh:
    with occ.Geometry() as geom:
        mesh_tubular(geom, joint)
        return geom.generate_mesh()