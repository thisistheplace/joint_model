from pydantic import BaseModel

from ..geometry import Point3D

class Node(BaseModel):
    name: str | None = None
    id: int
    coordinates: Point3D

class Nodes(BaseModel):
    nodes: dict[int, Node]