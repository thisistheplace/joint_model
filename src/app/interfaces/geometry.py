from pydantic import BaseModel


class Point3D(BaseModel):
    x: float = ...
    y: float = ...
    z: float = ...


class Vector3D(BaseModel):
    x: float = ...
    y: float = ...
    z: float = ...


class Axis3D(BaseModel):
    point: Point3D = ...
    vector: Vector3D = ...
