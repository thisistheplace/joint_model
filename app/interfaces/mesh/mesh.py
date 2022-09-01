from pydantic import BaseModel

from .nodes import Nodes
from .elements import Elements
from .sets import NodeSets, ElementSets

class Mesh(BaseModel):
    name: str | None = None
    nodes: Nodes
    elements: Elements
    node_sets: NodeSets
    element_sets: ElementSets