from collections import deque
from contextlib import contextmanager
from copy import deepcopy
import gmsh
import numpy as np
import scipy.interpolate as scipolate
from scipy.spatial.transform import Rotation as R

from app.interfaces.numpy.model import NpTubular

from .cylinder import add_cylinder
from ..geometry.vectors import unit_vector

from ...interfaces.geometry import *
from ...interfaces.mapper import map_to_np
from ...interfaces.model import *
from ...interfaces.mesh import *

FACTORY = gmsh.model.occ

# scipolate.Rbf()


def line_points(
    points_in: list[np.ndarray],
    interval: int | None = None,
    size: float | None = None,
    rtol: float = 1.0e-6,
    loop: bool = True
) -> deque[np.ndarray]:
    """Creates intermediary points between points at interval frequency or size.

    The order of the points is important and is maintained in the generated list of points.

    Args:
        points_in: list of numpy arrays of shape (3,)
        interval: number of intervals between adjacent points to create intermediary points
        size: size of distances between intermediary points
        rtol: relative tolerance used to determine if first and last points are the same
        loop: if True (default) then repeats the first point at the end to create a full loop

    Returns:
        deque of np.ndarray objects including all points (points and intermediary)
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

    points_out = deque()
    points_out.append(points_in[0])
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
            points_out.append(midpoint)
            distance += size

    # Add end of loop
    if loop and not np.isclose(points_in[0], points_in[-1], rtol=rtol).all():
        points_out.append(point2)
    elif loop and np.isclose(points_in[0], points_in[-1], rtol=rtol).all():
        points_out[-1] = points_out[0]

    return points_out


def add_flat_tube(tube: Tubular, specs: MeshSpecs) -> list[int, int]:
    """Make a flat mesh out of a tubular

    Initially create it in the x, y plane where 1 is at
    the tube.axis.point.

        5-------4-------3
        |               |
        |               |
        |               |
        |               |
        6-------1-------2
    y
    |
    |
    ------ x

    """
    nptube: NpTubular = map_to_np(tube)
    length = np.linalg.norm(nptube.axis.vector.array)

    pt1 = nptube.axis.point.array

    pt2 = deepcopy(pt1)
    pt2[0] += nptube.diameter / 2.0

    pt3 = deepcopy(pt1)
    pt3[0] += nptube.diameter / 2.0
    pt3[1] += length

    pt4 = deepcopy(pt1)
    pt4[1] += length

    pt5 = deepcopy(pt1)
    pt5[0] -= nptube.diameter / 2.0
    pt5[1] += length

    pt6 = deepcopy(pt1)
    pt6[0] -= nptube.diameter / 2.0

    # closed loop
    # NOTE: point order may need to be clockwise!
    key_points = [pt1, pt2, pt3, pt4, pt5, pt6, pt1]

    line_of_points = line_points(key_points, interval=specs.interval, size=specs.size)
    pnt_tags = [FACTORY.addPoint(*pnt.tolist()) for pnt in line_of_points]
    lines = [FACTORY.addLine(pnt, pnt_tags[idx + 1]) for idx, pnt in enumerate(pnt_tags[:-1])]
    curve = FACTORY.addCurveLoop(lines)
    surface = FACTORY.addSurfaceFilling(curve)
    FACTORY.synchronize()

    # We delete the source geometry, and increase the number of sub-edges for a
    # nicer display of the geometry:
    # FACTORY.remove([2, lines])
    FACTORY.remove([(1, curve)])
    # gmsh.option.setNumber("Geometry.NumSubEdges", 20)
    return [2, surface]

# def punch_holes()