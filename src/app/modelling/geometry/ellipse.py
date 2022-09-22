from typing import Generator
import gmsh
import math
import numpy as np
from scipy import optimize
import sympy

from .exceptions import GeometryException

FACTORY = gmsh.model.occ

# TODO: review this https://www.maplesoft.com/applications/Preview.aspx?id=3773


def ellipse_quadrant_points(
    centre: np.ndarray,
    radius_x: float,
    radius_y: float | None = None,
    interval: int | None = None,
    size: float | None = None,
    rtol: float = 1.0e-6,
) -> Generator[np.ndarray, np.ndarray, None]:
    """Creates points around an ellipse at interval frequency or size within the first quadrant.

    TODO: use a deterministic, non-iterative method to improve performance!

    Args:
        centre: numpy array defining ellipse centre, shape (2,)
        radius_x: float defining the radius in the x direction
        radius_y: float defining the radius in the y direction (if None, radius_x is taken)
        interval: number of intervals within a quadrant of the ellipse
        size: size of distances between intermediary points
        rtol: relative tolerance used to determine if first and last points are the same

    Returns:
        Generator of np.ndarray objects including all points (points and intermediary)
    """
    if (interval is not None and size is not None) or (
        interval is None and size is None
    ):
        raise ValueError(
            "Cannot provide values for intervals and size to add_line method"
        )
    if centre is None or radius_x is None:
        raise ValueError("Cannot create ellipse loop if centre or radius_x are None.")
    if radius_y is None:
        radius_y = radius_x

    # figure out start point
    start_point = sympy.Point2D([centre[0] + float(radius_x), centre[1]])
    start_angle = 0.0
    # Ellipse is 2D
    ellipse = sympy.Ellipse(centre[:2], radius_x, radius_y)
    # setup parametric next point
    param_angle = sympy.symbols("param_angle")
    param_point = ellipse.arbitrary_point(param_angle)
    # determine increment size / segment length
    if interval is not None:
        size = ellipse.circumference.evalf() / 4.0 / abs(interval)
    # TODO: stop being lazy and calculate points at quadrant 1 then rotate 3 times to get the remaining
    # which should avoid scipy.optimize needing to be called so frequently
    yield np.array(start_point, dtype=float)
    while True:
        pnt_angle = ellipse_segment_angle(ellipse, start_point, start_angle, size, rtol)
        if pnt_angle >= math.pi / 2.0:
            pnt_angle = math.pi / 2.0
            next_point: sympy.Point2D = param_point.subs(param_angle, pnt_angle)
            return np.array(next_point.coordinates, dtype=float)
        next_point: sympy.Point2D = param_point.subs(param_angle, pnt_angle)
        yield np.array(next_point.coordinates, dtype=float)
        start_point = next_point
        start_angle = pnt_angle


def ellipse_segment_angle(
    ellipse: sympy.Ellipse,
    start: sympy.Point2D,
    start_angle: float,
    length: float,
    rtol=1e-8,
) -> float:
    """Calculate the angle associated with a segment length within a 180.0 degree range

    Process is iterative using scipy.optimize.minimize

    Args:
        ellipse: sympy.Ellipse object
        start: sympy.Point2D on circumference where length is measured from
        start_angle: float angle of start point in radians
        length: float defining the target straight length of the segment
        rtol: numerical tolerance for solver

    Returns float angle of point at segment length from start
    """
    angle: sympy.Symbol = sympy.symbols("angle")
    pnt: sympy.Point2D = ellipse.arbitrary_point(angle)
    solution: optimize.OptimizeResult = optimize.minimize_scalar(
        _iter_ellipse_angle,
        args=(pnt, angle, start, length),
        method="bounded",
        bounds=[start_angle - abs(rtol), math.pi / 2.0 + start_angle + abs(rtol)],
        options={"xatol": rtol},
    )
    # manual check
    point_found = pnt.subs(angle, solution.x)
    segment = start.distance(point_found).evalf()
    if not solution.success or abs(segment - length) > rtol:
        msg = (
            f"Could not find point along tubular insect with details:\n"
            f"\tstart: {np.array(start.coordinates, dtype=float)}\n"
            f"\tpoint: {np.array(point_found.coordinates, dtype=float)}\n"
            f"\tangle: {solution.x}\n"
            f"\tlength: {length}"
        )
        # TODO: maybe this should be a logged warning?
        raise GeometryException(msg)
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
    return points.dot(R.T)


def _iter_ellipse_angle(
    input: float,
    para_point: sympy.Point2D,
    angle: sympy.Symbol,
    start: sympy.Point2D,
    length: float,
):
    next_point = para_point.subs(angle, input)
    segment = start.distance(next_point).evalf()
    # explicit float type since scipy.core.numbers.Float does not play nicely with np.isnan
    return float(abs(length - segment))
