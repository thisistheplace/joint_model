from inspect import isclass
from pydantic import BaseModel
from pydantic.main import ModelMetaclass
import pytest
import sys
from typing import Any

sys.path.append("/src")

from app.interfaces import *
from app.interfaces.mapper import map_to_np
from app.interfaces.examples.joints import EXAMPLE_MODELS


@pytest.fixture
def model() -> Model:
    return EXAMPLE_MODELS["TJoint"]


class TestMapper:
    def _get_type(self, model: BaseModel, target: Any) -> Any:
        if type(model) is target:
            return model
        for attr_name in model.dict().keys():
            attr = getattr(model, attr_name)
            if isinstance(type(attr), ModelMetaclass):
                if type(attr) is target:
                    return attr
                else:
                    found = self._get_type(attr, target)
                    if type(found) is target:
                        return found
            if isinstance(attr, list):
                for obj in attr:
                    found = self._get_type(obj, target)
                    if type(found) is target:
                        return found

    def find_type(self, model: BaseModel, target: Any) -> Any:
        found = self._get_type(model, target)
        if found is None:
            raise TypeError(f"Could not find type {target} in {type(model)}")
        return found

    def test_map_point3D(self, model):
        found = self.find_type(model, Point3D)
        assert isinstance(map_to_np(found), NpPoint3D)

    def test_map_axis3D(self, model):
        found = self.find_type(model, Axis3D)
        assert isinstance(map_to_np(found), NpAxis3D)

    def test_map_tubular(self, model):
        found = self.find_type(model, Tubular)
        assert isinstance(map_to_np(found), NpTubular)

    def test_map_joint(self, model):
        found = self.find_type(model, Joint)
        assert isinstance(map_to_np(found), NpJoint)

    def test_map_model(self, model):
        found = self.find_type(model, Model)
        assert isinstance(map_to_np(found), NpModel)
