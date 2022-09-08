from pydantic import ValidationError
import pytest
import sys

sys.path.append("/src")

from app.interfaces.model import Model
from app.interfaces.geometry import Point3D
from app.interfaces.validation import validate_and_convert_json
from app.interfaces.examples.joints import EXAMPLE_MODELS


@pytest.fixture
def point():
    return Point3D(x=1.0, y=2.0, z=3.0)


class TestValidateAndConvertJson:
    def test_valid_conversion(self, point):
        assert point == validate_and_convert_json(point.dict(), Point3D)

    def test_validates_json_string(self, point):
        # .json() returns a string of the json data
        assert point == validate_and_convert_json(point.json(), Point3D)

    def test_validates_object(self, point):
        assert point == validate_and_convert_json(point, Point3D)

    def test_validates_model(self):
        assert EXAMPLE_MODELS["TJoint"] == validate_and_convert_json(
            EXAMPLE_MODELS["TJoint"], Model
        )

    def test_invalid_conversion(self):
        with pytest.raises(ValidationError):
            validate_and_convert_json(EXAMPLE_MODELS["TJoint"], Point3D)

    def test_invalid_input_type(self):
        with pytest.raises(ValidationError):
            validate_and_convert_json(None, Point3D)

    def test_invalid_target_type(self):
        with pytest.raises(TypeError):
            validate_and_convert_json(EXAMPLE_MODELS["TJoint"], str)
