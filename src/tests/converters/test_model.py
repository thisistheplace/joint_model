import io
import pygmsh
import pytest

import sys
sys.path.append("/src")

from app.interfaces import *
from app.converters.model import mesh_joint, mesh_tubular

@pytest.fixture
def geom():
    with pygmsh.occ.Geometry() as geom:
        yield geom


class TestMeshTubular:
    def test_mesh_tubular(self, geom: pygmsh.occ.Geometry):
        tube = Tubular(
            name="test",
            axis= Axis3D(
                point=Point3D(
                    x=1,
                    y=1,
                    z=1
                ),
                vector=Vector3D(
                    x=0,
                    y=0,
                    z=3
                )
            ),
            diameter=0.5
        )
        cylinder = mesh_tubular(geom, tube)

        assert cylinder is not None
        mesh = geom.generate_mesh()
        # mesh.write("abaqus.inp", "ansys")
        # with open("abaqus.inp", "r") as f:
        #     print(f.readlines())
        assert mesh is not None