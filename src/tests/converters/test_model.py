import os
from pathlib import Path

import pytest
import shutil

import sys

sys.path.append("/src")

from app.interfaces import *
from app.modelling.mesher.mesh import mesh_model
from app.converters.mesh import mesh_to_dash_vtk
from app.viewer.models import DEMO_MODELS

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
        joint = DEMO_MODELS["TJoint"]
        with mesh_model(joint) as mesh:
            mesh_to_dash_vtk(mesh)
            assert mesh is not None

        assert 1 == 0
