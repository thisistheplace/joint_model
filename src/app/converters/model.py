from .mesh import mesh_to_dash_vtk

from ..interfaces import *
from ..modelling.mesher.mesh import mesh_model


def convert_joint_to_dash_vtk(joint: Joint) -> dict[str, list]:
    with mesh_model(joint) as mesh:
        return mesh_to_dash_vtk(mesh)
