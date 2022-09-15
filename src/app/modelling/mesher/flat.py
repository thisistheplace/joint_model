from copy import deepcopy
import gmsh
import math
import numpy as np

from app.interfaces.numpy.model import NpTubular

from ..geometry.line import line_points

from ...interfaces.geometry import *
from ...interfaces.mapper import map_to_np
from ...interfaces.model import *
from ...interfaces.mesh import *

FACTORY = gmsh.model.occ

# scipolate.Rbf()
def add_flat_tube(tube: Tubular, specs: MeshSpecs) -> list[int, int]:
    """Make a flat mesh out of a tubular

    Initially create it in the Y/Z plane where 1 is at
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
    circumference = math.pi * nptube.diameter

    pt1 = nptube.axis.point.array

    pt2 = deepcopy(pt1)
    pt2[1] += circumference / 2.0

    pt3 = deepcopy(pt1)
    pt3[1] += circumference / 2.0
    pt3[2] += length

    pt4 = deepcopy(pt1)
    pt4[2] += length

    pt5 = deepcopy(pt1)
    pt5[1] -= circumference / 2.0
    pt5[2] += length

    pt6 = deepcopy(pt1)
    pt6[1] -= circumference / 2.0

    print(f"Height: {length}")
    print(f"Width: {circumference}")

    # closed loop
    # NOTE: point order may need to be clockwise!
    key_points = [pt1, pt2, pt3, pt4, pt5, pt6, pt1]

    line_of_points = list(
        line_points(key_points, interval=specs.interval, size=specs.size)
    )

    pnt_tags = [FACTORY.addPoint(*pnt.tolist()) for pnt in line_of_points]
    lines = [
        FACTORY.addLine(pnt, pnt_tags[idx + 1]) for idx, pnt in enumerate(pnt_tags[:-1])
    ]
    curve = FACTORY.addCurveLoop(lines)
    surface = FACTORY.addSurfaceFilling(curve)
    FACTORY.synchronize()

    # We delete the source geometry, and increase the number of sub-edges for a
    # nicer display of the geometry:
    for l in lines:
        FACTORY.remove([(1, l)])
    FACTORY.remove([(1, curve)])
    FACTORY.synchronize()
    # gmsh.option.setNumber("Geometry.NumSubEdges", 20)
    return [2, surface]


# def punch_holes()
