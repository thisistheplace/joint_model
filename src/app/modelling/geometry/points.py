from collections import deque
from typing import Generator
import gmsh
import numpy as np
from scipy import optimize
import sympy

from ..geometry.vectors import unit_vector

FACTORY = gmsh.model.occ

class GeometryException(Exception):
    pass

def line_points(
    points_in: list[np.ndarray],
    interval: int | None = None,
    size: float | None = None,
    rtol: float = 1.0e-6,
    loop: bool = True
) -> Generator[np.ndarray, np.ndarray, None]:
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

    # check whether first and last point are the sameg
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
        while distance <= length or abs(distance - length) < rtol:
            midpoint = point1 + distance * unit
            yield midpoint
            distance += size
        if not np.allclose(midpoint, point2, rtol=rtol):
            yield point2

def ellipse_points(
    centre: np.ndarray,
    radius_x: float,
    radius_y: float | None = None,
    interval: int | None = None,
    size: float | None = None,
    rtol: float = 1.0e-6
) -> Generator[np.ndarray, np.ndarray, None]:
    """Creates points around an ellipse at interval frequency or size.

    Always creates a closed loop.

    Args:
        centre: numpy array defining ellipse centre, shape (3,)
        radius_x: float defining the radius in the x direction
        radius_y: float defining the radius in the y direction (if None, radius_x is taken)
        interval: number of intervals between adjacent points to create intermediary points
        size: size of distances between intermediary points
        rtol: relative tolerance used to determine if first and last points are the same

    Returns:
        Generator of np.ndarray objects including all points (points and intermediary)
    """
    if (interval is not None and size is not None) or (interval is None and size is None):
        raise ValueError(
            "Cannot provide values for intervals and size to add_line method"
        )
    if centre is None or radius_x is None:
        raise ValueError("Cannot create ellipse loop if centre or radius_x are None.")
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
        while distance <= length or abs(distance - length) < rtol:
            midpoint = point1 + distance * unit
            yield midpoint
            distance += size
        if not np.allclose(midpoint, point2, rtol=rtol):
            yield point2

def _point_distance(pnt1: np.ndarray, pnt2: np.ndarray, rtol: float) -> float:
    vector = pnt2 - pnt1
    if np.allclose(vector, [0.0, 0.0], rtol=rtol):
        return 0.0
    return np.linalg.norm(vector)

def _iter_ellipse_angle(input: float, para_point: sympy.Point2D, angle: sympy.Symbol, start: np.ndarray, length: float, rtol: float):
    point = para_point.subs(angle, input)
    segment = _point_distance(np.array(point.coordinates, dtype=float), start, rtol)
    return abs(length - segment)

def ellipse_segment_angle(ellipse: sympy.Ellipse, start: np.ndarray, length: float, rtol=1e-8) -> float:
    """Calculate the angle associated with a segment length
    
    Process is iterative using scipy.optimize.minimize

    Args:
        ellipse: sympy.Ellipse object
        start: numpy array defining 2D point on circumference length is measured from
        length: float defining the target straight length of the segment
        rtol: numerical tolerance for solver

    Returns float angle at length from start
    """
    # check start point is on ellipse circumference
    start_point = sympy.Point2D(start)
    if not check_ellipse_intersect(ellipse, start_point):
        raise GeometryException(f"Starting point {start_point} does not intersect ellipse circumference {ellipse}")
    angle: sympy.Symbol = sympy.symbols("angle")
    pnt: sympy.Point2D = ellipse.arbitrary_point(angle)
    solution: optimize.OptimizeResult = optimize.minimize_scalar(_iter_ellipse_angle, args=(pnt, angle, start, length, rtol), tol=rtol)
    # manual check
    angle_found = np.array(pnt.subs(angle, solution.x).coordinates, dtype=float)
    segment = _point_distance(angle_found, start, rtol)
    if not solution.success or abs(segment - length) > rtol:
        # TODO: maybe this should be a logged warning?
        raise GeometryException(f"Could not find point along tubular insect for arc length {length}")
    return solution.x

def check_ellipse_intersect(ellipse: sympy.Ellipse, point: sympy.Point2D) -> bool:
    return len(ellipse.intersection(point)) == 1

def rotate_points(points: np.ndarray, angle: float) -> np.ndarray:
    """Rotate array of 2D coordinates clockwise by angle about centre point (Z axis)
    
    Args:
        points: array of 2D points to rotate shape (2, N)
        centre: array of 2D centre of rotation, shape (2,)
        angle: float defining clockwise rotation radians angle about Z axis (out of plane)

    Returns array of rotated points shape (2, N)
    """
    c, s = np.cos(angle), np.sin(angle)
    R = np.array(((c, -s), (s, c)))
    print(points)
    print(R.T)
    return points.dot(R.T)

def ellipse_point(ellipse: sympy.Ellipse, angle: float) -> np.ndarray:
    """Calculate the coordinates on the circumference of an ellipse at angle
    
    Args:
        ellipse: sympy.Ellipse object
        angle: float defining the angle to calculate the circumferential point

    Returns 3D coordinates of circumferential point
    """