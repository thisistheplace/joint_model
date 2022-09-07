from pydantic import BaseModel

from .geometry import Joint


class Model(BaseModel):
    name: str = ...
    joint: Joint = ...
