from pydantic import BaseModel

class Point3D(BaseModel):
    name: str | None = None
    x: float
    y: float
    z: float

class Vector3D(BaseModel):
    name: str | None = None
    x: float
    y: float
    z: float

class Axis3D(BaseModel):
    name: str | None = None
    point: Point3D
    vector: Vector3D