from pydantic import BaseModel


class Set(BaseModel):
    name: str


class NodeSet(Set):
    # how to check that node_ids are in the Nodes array
    node_ids: list[int] = ...


class NodeSets(BaseModel):
    sets: dict[str, NodeSet] = ...


class ElementSet(Set):
    element_ids: list[int] = ...


class ElementSets(BaseModel):
    sets: dict[str, ElementSet] = ...
