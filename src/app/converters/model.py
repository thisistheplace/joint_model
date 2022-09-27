from .mesh import mesh_to_dash_vtk, ElementType

from ..interfaces import *
from ..modelling.mesher.mesh import mesh_model


def convert_model_to_dash_vtk(model: Model) -> DashVtkModel:
    with mesh_model(model, MeshSpecs(size=0.1)) as mesh:
        mesh = mesh_to_dash_vtk(mesh, ElementType.TRIANGLE)
        return DashVtkModel(name=model.name, mesh=mesh)
