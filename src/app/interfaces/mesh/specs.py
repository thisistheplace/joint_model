"""Defines common specs for meshing"""
from pydantic import BaseModel


class MeshSpecs(BaseModel):
    # Add some validation here for OneOf
    size: float | None = None
    interval: float | None = None
