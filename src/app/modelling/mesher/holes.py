import gmsh
import numpy as np

from ...interfaces import *
from ...interfaces.mapper import map_to_np
from ..geometry.weld import get_weld_intersect_points

FACTORY = gmsh.model.occ


def hole_curve(master: Tubular, slave: Tubular) -> dict[str, np.ndarray]:
    pnt_tags = [
        FACTORY.addPoint(*pnt.tolist())
        for pnt in get_weld_intersect_points(map_to_np(master), map_to_np(slave))
    ]
    # make sure last point is the same as the first point
    pnt_tags = pnt_tags[:15]
    pnt_tags[-1] = pnt_tags[0]
    FACTORY.synchronize()
    lines = [
        FACTORY.addLine(pnt, pnt_tags[idx + 1]) for idx, pnt in enumerate(pnt_tags[:-1])
    ]
    return FACTORY.addCurveLoop(lines)