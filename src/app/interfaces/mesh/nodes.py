from pydantic import BaseModel

from ..geometry import Point3D


class Node(BaseModel):
    id: int = ...
    coordinates: Point3D = ...


class Nodes(BaseModel):
    nodes: dict[int, Node] = ...
