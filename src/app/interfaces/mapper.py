from typing import Any
import numpy as np

from . import *

def interface_to_np(inter: Any):
    match type(inter):
        case type(Point3D):
            return NpPoint3D(
                array=np.array([inter.x, inter.y, inter.z])
            )
        case type(Vector3D):
            return NpVector3D(
                array=np.array([inter.x, inter.y, inter.z])
            )
        case type(Axis3D):
            return NpAxis3D(
                point=np.array([inter.point.x, inter.point.y, inter.point.z]),
                vector=np.array([inter.vector.x, inter.vector.y, inter.vector.z])
            )
        case type(Tubular):
            return NpTubular(
                name=inter.name,
                axis=interface_to_np(inter.axis),
                diameter=inter.diameter
            )
        case type(Joint):
            return NpJoint(
                name=inter.name,
                tubes=[interface_to_np(tube) for tube in inter.tubes],
                origin=interface_to_np(inter.origin)
            )
        case type(Model):
            return NpModel(
                name=inter.name,
                joint=interface_to_np(inter.model)
            )
        case _:
            raise TypeError(f"Could not match interface type {type(inter)} and numpy types")