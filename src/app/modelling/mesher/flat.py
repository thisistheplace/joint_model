from collections import deque
from contextlib import contextmanager
from copy import deepcopy
import gmsh
import numpy as np
import scipy.interpolate as scipolate
from scipy.spatial.transform import Rotation as R

from app.interfaces.numpy.model import NpTubular

from .cylinder import add_cylinder
from .specs import MeshSpecs
from .vectors import unit_vector

from ...interfaces.geometry import *
from ...interfaces.mapper import map_to_np
from ...interfaces.model import *

FACTORY = gmsh.model.occ

# scipolate.Rbf()


def line_points(
    points_in: list[np.ndarray],
    interval: int | None = None,
    size: float | None = None,
    rtol: float = 1.0e-6,
    loop: bool = True
) -> deque[np.ndarray]:
    """Creates intermediary points between points at interval frequency or size and adds line.

    The order of the points is important and is maintained in the generated line.

    Args:
        points_in: list of numpy arrays of shape (3,)
        interval: number of intervals between adjacent points to create intermediary points
        size: size of distances between intermediary points
        rtol: relative tolerance used to determine if first and last points are the same
        loop: if True (default) then repeats the first point at the end to create a full loop

    Returns:
        deque of np.ndarray objects including all points (points and intermediary)
    """
    if interval is not None and size is not None:
        raise ValueError(
            "Cannot provide values for intervals and size to add_line method"
        )
    if len(points_in) < 2:
        raise ValueError("Cannot create line between less than 2 points")

    # check whether first and last point are the same
    if not np.isclose(points_in[0], points_in[-1], rtol=rtol).all() and loop:
        points_in = points_in + [points_in[0]]

    points_out = deque()
    for idx in range(len(points_in) - 1):
        point1 = points_in[idx]
        points_out.append(point1)
        point2 = points_in[idx + 1]
        vector = point2 - point1
        length = np.linalg.norm(vector)
        unit = unit_vector(vector)
        if interval is not None:
            size = length / abs(interval)
        distance = 0.0
        distance += size
        while distance < length:
            midpoint = point1 + distance * unit
            points_out.append(midpoint)
            distance += size

    # Add end of loop
    if loop:
        points_out.append(point2)
    return points_out


def flatten_tube(tube: Tubular, specs: MeshSpecs):
    """Make a flat mesh out of a tubular

    Initially create it in the x, y plane where 1 is at
    the tube.axis.point.

        4---------------3
        |               |
        |               |
        |               |
        |               |
        5-------1-------2
    y
    |
    |
    ------ x

    """
    nptube: NpTubular = map_to_np(tube)
    length = np.linalg.norm(nptube.axis.vector.array)

    pt1 = nptube.axis.point

    pt2 = deepcopy(pt1)
    pt2[0] += nptube.diameter / 2.0

    pt3 = deepcopy(pt1)
    pt3[0] += nptube.diameter / 2.0
    pt3[1] += length

    pt4 = deepcopy(pt1)
    pt4[0] -= nptube.diameter / 2.0
    pt4[1] += length

    pt5 = deepcopy(pt1)
    pt5[0] -= nptube.diameter / 2.0

    origin = tube.axis.point
    vector = tube.axis.vector
    start = FACTORY.addPoint(
        origin.x,
        origin.y,
        origin.z,
    )
    end = FACTORY.addPoint(
        origin.x + vector.x, origin.y + vector.y, origin.z + vector.z
    )
    extrusion = FACTORY.addSpline([start, end])
    wire = FACTORY.addWire([extrusion])

    # Create disk in x, y plane then transform it to be perpendicular
    # to the wire
    radius = tube.diameter / 2.0
    ring = FACTORY.addCircle(origin.x, origin.y, origin.z, radius)
    rotatexy([(1, ring)], origin, vector)
    pipe = FACTORY.addPipe([(1, ring)], wire)

    # We delete the source surface, and increase the number of sub-edges for a
    # nicer display of the geometry:
    FACTORY.remove([(1, ring)])
    FACTORY.remove([(1, extrusion)])
    gmsh.option.setNumber("Geometry.NumSubEdges", 20)
    return pipe[0]
