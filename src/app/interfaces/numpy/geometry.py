import numpy as np

from .base import NpBaseModel


class NpPoint3D(NpBaseModel):
    array: np.ndarray


class NpVector3D(NpBaseModel):
    array: np.ndarray


class NpAxis3D(NpBaseModel):
    point: NpPoint3D = ...
    vector: NpVector3D = ...
