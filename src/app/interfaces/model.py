from pydantic import BaseModel

from .geometry import Joint
from .examples.joints import EXAMPLE_JOINTS


class Model(BaseModel):
    name: str = ...
    joint: Joint = ...

    class Config:
        schema_extra = {"name": "TJoint", "joint": EXAMPLE_JOINTS["TJoint"].json()}
