import io
import os
from pathlib import Path
import pygmsh
import pytest
import shutil

import sys
sys.path.append("/src")

from app.interfaces import *
from app.converters.model import mesh_joint, mesh_tubular

TEMP = ".temp/converters"

@pytest.fixture
def geom():
    with pygmsh.occ.Geometry() as geom:
        yield geom

@pytest.fixture
def temp_dir():
    temp_path = Path(TEMP).resolve()
    os.makedirs(temp_path)
    yield temp_path
    shutil.rmtree(temp_path)


@pytest.mark.usefixtures("temp_dir")
class TestMeshTubular:

    def test_mesh_tubular(self, geom: pygmsh.occ.Geometry, temp_dir: Path):
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
        assert mesh is not None
        
        # This seems to require a file to touch disk
        out = io.FileIO(str(temp_dir / "test.vtk"), "wb+")
        mesh.write(out, "vtk")
        out.seek(0)
        bdata = out.readlines()
        assert bdata is not None