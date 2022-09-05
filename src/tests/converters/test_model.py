import os
from pathlib import Path

import pytest
import shutil

import sys
sys.path.append("/src")

from app.interfaces import *
from app.mesher.mesh import mesh_model
from app.converters.mesh import mesh_to_dash_vtk

TEMP = ".temp/converters"

@pytest.fixture
def temp_dir():
    temp_path = Path(TEMP).resolve()
    os.makedirs(temp_path)
    yield temp_path
    shutil.rmtree(temp_path)

@pytest.mark.usefixtures("temp_dir")
class TestMeshTubular:

    def test_mesh_tubular(self, temp_dir: Path):
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
        joint = Joint(
            name="test",
            tubes=[tube]
        )

        with mesh_model(joint) as mesh:
            assert mesh is not None