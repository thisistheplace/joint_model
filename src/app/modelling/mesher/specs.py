"""Defines common specs for meshing"""
from pydantic import BaseModel


class MeshSpecs(BaseModel):
    size = float
