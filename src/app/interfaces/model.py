from pydantic import BaseModel

from .geometry import Axis3D, Point3D


class Tubular(BaseModel):
    name: str = ...
    axis: Axis3D = ...
    diameter: float = ...


class Joint(BaseModel):
    name: str = ...
    tubes: list[Tubular] = ...
    origin: Point3D | None = None
