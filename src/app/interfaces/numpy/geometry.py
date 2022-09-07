from pydantic import BaseModel
import numpy as np

class NpPoint3D(BaseModel):
    array: np.ndarray


class NpVector3D(BaseModel):
    array: np.ndarray


class NpAxis3D(BaseModel):
    point: NpPoint3D = ...
    vector: NpVector3D = ...