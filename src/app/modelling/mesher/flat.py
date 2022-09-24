from copy import deepcopy
import gmsh
import math
import numpy as np

from app.interfaces.numpy.model import NpTubular

from ..geometry.line import line_points
from .holes import hole_curve
from ..geometry.weld import get_weld_intersect_points

from ...interfaces.geometry import *
from ...interfaces.mapper import map_to_np
from ...interfaces.model import *
from ...interfaces.mesh import *

FACTORY = gmsh.model.occ

# scipolate.Rbf()
def add_flat_tube(
    master: Tubular, slaves: list[Tubular], specs: MeshSpecs
) -> list[int, int]:
    """Make a flat mesh out of a tubular

    Initially create it in the X/Z plane where 1 is at
    the master.axis.point + radius (in Y direction).

        5-------4-------3
        |               |
        |               |
        |               |
        |               |
        6-------1-------2
    Z
    |
    |
    ------ x

    """
    nptube: NpTubular = map_to_np(master)
    length = np.linalg.norm(nptube.axis.vector.array)
    circumference = math.pi * nptube.diameter

    pt1 = nptube.axis.point.array
    pt1[1] = nptube.diameter / 2.0

    pt2 = deepcopy(pt1)
    pt2[0] += circumference / 2.0

    pt3 = deepcopy(pt1)
    pt3[0] += circumference / 2.0
    pt3[2] += length

    pt4 = deepcopy(pt1)
    pt4[2] += length

    pt5 = deepcopy(pt1)
    pt5[0] -= circumference / 2.0
    pt5[2] += length

    pt6 = deepcopy(pt1)
    pt6[0] -= circumference / 2.0

    # closed loop
    # NOTE: point order may need to be clockwise!
    key_points = [pt1, pt2, pt3, pt4, pt5, pt6, pt1]

    line_of_points = list(
        line_points(key_points, interval=specs.interval, size=specs.size)
    )
    
    # weld_pnts = []
    # for pnts in [list(get_weld_intersect_points(map_to_np(master), map_to_np(slave))) for slave in slaves]:
    #     weld_pnts += pnts
    # points = line_of_points + weld_pnts
    # x = [pnt[0] for pnt in points]
    # y = [pnt[1] for pnt in points]
    # z = [pnt[2] for pnt in points]
    # import plotly.express as px
    # fig = px.scatter_3d(x=x, y=y, z=z)
    # fig.show()

    # raise TypeError()

    pnt_tags = [FACTORY.addPoint(*pnt.tolist()) for pnt in line_of_points]
    lines = [
        FACTORY.addLine(pnt, pnt_tags[idx + 1]) for idx, pnt in enumerate(pnt_tags[:-1])
    ]
    perimeter = FACTORY.addCurveLoop(lines)

    # get curves defining holes
    holes = [hole_curve(master, slave) for slave in slaves]

    surface = FACTORY.addPlaneSurface([perimeter] + holes)

    FACTORY.synchronize()

    # for curve in holes:
    #     gmsh.model.mesh.embed(1, [curve], 2, surface)

    # We delete the source geometry, and increase the number of sub-edges for a
    # nicer display of the geometry:
    # for l in lines:
    #     FACTORY.remove([(1, l)])
    # FACTORY.remove([(1, perimeter)])
    FACTORY.synchronize()
    # gmsh.option.setNumber("Geometry.NumSubEdges", 20)
    return [2, surface]


# def punch_holes()
