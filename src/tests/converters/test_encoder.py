import os
from pathlib import Path
import json
import numpy as np
import pytest
import shutil
import sys

sys.path.append("/src")

from app.converters.encoder import NpEncoder


@pytest.fixture
def data():
    return {"a": 1, "b": 2, "c": {"d": "test", "e": 3.112, "f": [1.1, 2.0]}}


class TestJsonNpEncoder:
    def test_no_numpy_passes(self, data):
        encoded = json.dumps(data, cls=NpEncoder)
        assert json.loads(encoded) == data

    def test_numpy_data_passes(self, data):
        data_np = {
            "a": np.int64(1),
            "b": np.int64(2),
            "c": {
                "d": "test",
                "e": np.float64(3.112),
                "f": np.array([np.float64(1.1), np.float64(2.0)]),
            },
        }
        encoded = json.dumps(data_np, cls=NpEncoder)
        assert json.loads(encoded) == data
