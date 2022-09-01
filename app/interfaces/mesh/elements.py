from pydantic import BaseModel

from ..geometry import Vector3D

class Element(BaseModel):
    name: str | None = None
    id: int
    # The order matters here
    nodes: list[int]

class ShellElement(Element):
    # Points from inside to outside element surfaces
    normal: Vector3D

class Elements(BaseModel):
    elements: dict[int, Element]