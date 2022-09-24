import numpy as np
from scipy.spatial.transform import Rotation
from typing import Any


def unit_vector(vector: list[Any]):
    """Returns the unit vector of the vector."""
    return vector / np.linalg.norm(vector)


def angle_between_vectors(v1, v2):
    """Returns the angle in radians between vectors 'v1' and 'v2'::

    >>> angle_between((1, 0, 0), (0, 1, 0))
    1.5707963267948966
    >>> angle_between((1, 0, 0), (1, 0, 0))
    0.0
    >>> angle_between((1, 0, 0), (-1, 0, 0))
    3.141592653589793
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    angle = np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))
    if np.isnan(angle):
        return 0.0
    return angle


def rotate(vector: np.ndarray, axis: np.ndarray, angle: float) -> np.ndarray:
    rotation_vector = angle * unit_vector(axis)
    rotation = Rotation.from_rotvec(rotation_vector)
    return rotation.apply(vector)


def unit_perp_vector(vector: np.ndarray) -> np.ndarray:
    vector = unit_vector(vector)
    if vector[1] != 0.0 or vector[2] != 0.0:
        temp = np.array([1.0, 0.0, 0.0])
    else:
        temp = np.array([0.0, 1.0, 0.0])
    return unit_vector(np.cross(vector, temp))