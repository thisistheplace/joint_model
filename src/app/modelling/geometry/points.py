from collections import deque
from typing import Generator
import gmsh
import numpy as np

from ..geometry.vectors import unit_vector

FACTORY = gmsh.model.occ

def line_points(
    points_in: list[np.ndarray],
    interval: int | None = None,
    size: float | None = None,
    rtol: float = 1.0e-6,
    loop: bool = True
) -> Generator[np.ndarray, None, None]:
    """Creates intermediary points in a straight line between points at interval frequency or size.

    The order of the points is important and is maintained in the generated list of points.

    Args:
        points_in: list of numpy arrays of shape (3,)
        interval: number of intervals between adjacent points to create intermediary points
        size: size of distances between intermediary points
        rtol: relative tolerance used to determine if first and last points are the same
        loop: if True (default) then repeats the first point at the end to create a full loop

    Returns:
        Generator of np.ndarray objects including all points (points and intermediary)
    """
    if (interval is not None and size is not None) or (interval is None and size is None):
        raise ValueError(
            "Cannot provide values for intervals and size to add_line method"
        )
    if len(points_in) < 2:
        raise ValueError("Cannot create line between less than 2 points")

    # check whether first and last point are the same
    if not np.isclose(points_in[0], points_in[-1], rtol=rtol).all() and loop:
        points_in = points_in + [points_in[0]]

    first = points_in[0]
    yield first
    for idx in range(len(points_in) - 1):
        point1 = points_in[idx]
        point2 = points_in[idx + 1]
        vector = point2 - point1
        length = np.linalg.norm(vector)
        unit = unit_vector(vector)
        if interval is not None:
            size = length / abs(interval)
        distance = 0.0
        distance += size
        while distance < length or abs(distance - length) < rtol:
            midpoint = point1 + distance * unit
            yield midpoint
            distance += size

    # Add end of loop
    if loop and not np.isclose(points_in[0], points_in[-1], rtol=rtol).all():
        yield point2
    elif loop and np.isclose(points_in[0], points_in[-1], rtol=rtol).all():
        yield first

def loop_points(
    points_in: list[np.ndarray],
    interval: int | None = None,
    size: float | None = None,
    rtol: float = 1.0e-6,
    loop: bool = True
) -> Generator[np.ndarray, None, None]:
    """Creates points around an oval at interval frequency or size.

    The order of the points is important and is maintained in the generated list of points.

    Args:
        points_in: list of numpy arrays of shape (3,)
        interval: number of intervals between adjacent points to create intermediary points
        size: size of distances between intermediary points
        rtol: relative tolerance used to determine if first and last points are the same
        loop: if True (default) then repeats the first point at the end to create a full loop

    Returns:
        Generator of np.ndarray objects including all points (points and intermediary)
    """
    if (interval is not None and size is not None) or (interval is None and size is None):
        raise ValueError(
            "Cannot provide values for intervals and size to add_line method"
        )
    if len(points_in) < 2:
        raise ValueError("Cannot create line between less than 2 points")

    # check whether first and last point are the same
    if not np.isclose(points_in[0], points_in[-1], rtol=rtol).all() and loop:
        points_in = points_in + [points_in[0]]

    first = points_in[0]
    yield first
    for idx in range(len(points_in) - 1):
        point1 = points_in[idx]
        point2 = points_in[idx + 1]
        vector = point2 - point1
        length = np.linalg.norm(vector)
        unit = unit_vector(vector)
        if interval is not None:
            size = length / abs(interval)
        distance = 0.0
        distance += size
        while distance < length or abs(distance - length) < rtol:
            midpoint = point1 + distance * unit
            yield midpoint
            distance += size

    # Add end of loop
    if loop and not np.isclose(points_in[0], points_in[-1], rtol=rtol).all():
        yield point2