from typing import Any
import numpy as np

from . import *

def _map_point(input: Point3D):
    return NpPoint3D(array=np.array([input.x, input.y, input.z]))

def _map_vector(input: Vector3D):
    return NpVector3D(array=np.array([input.x, input.y, input.z]))

def _map_axis(input: Axis3D):
    return NpAxis3D(
        point=map_to_np(input.point),
        vector=map_to_np(input.vector)
    )

def _map_tubular(input: Tubular):
    return NpTubular(
        name=input.name,
        axis=map_to_np(input.axis),
        diameter=input.diameter,
    )

def _map_joint(input: Joint):
    return NpJoint(
        name=input.name,
        tubes=[map_to_np(tube) for tube in input.tubes],
        origin=map_to_np(input.origin),
    )

def _map_model(input: Model):
    return NpModel(name=input.name, joint=map_to_np(input.model))

def _not_found(input: Any):
    raise TypeError(
        f"Could not match inputface type {type(input)} and numpy types"
    )

def map_to_np(input: Any) -> Any:
    mappers = {
        Point3D: _map_point,
        Vector3D: _map_vector,
        Axis3D: _map_axis,
        Tubular: _map_tubular,
        Joint: _map_joint,
        Model: _map_model
    }
    return mappers.get(type(input), _not_found)(input)