import gmsh
import numpy as np

from ...interfaces import *
from ...interfaces.mapper import map_to_np
from ..geometry.weld import get_weld_intersect_points
from ..geometry.intersections import flat_tube_intersection

FACTORY = gmsh.model.occ


def hole_curve(master: Tubular, slave: Tubular) -> dict[str, np.ndarray]:
    npmaster = map_to_np(master)
    npslave = map_to_np(slave)

    angle = 10
    num_points = int(360 / angle)
    hole_pnt_tags = []
    pnts = np.empty((num_points, 3))
    hole_points = []
    for idx, pnt in enumerate(
        get_weld_intersect_points(npmaster, npslave, angle_inc=angle)
    ):
        hole_points.append(pnt)
        hole_pnt_tags.append(FACTORY.addPoint(*pnt.tolist()))
        pnts[idx, :] = pnt

    flat_intersect = flat_tube_intersection(npmaster, npslave)

    # Vectors from center points to points
    vectors = pnts - flat_intersect
    unit_vectors = (vectors.T / np.linalg.norm(vectors, axis=1)).T

    # create points at radial distances away from hole points
    distances = [0.05, 0.1, 0.15, 0.2]
    rad_lines = []
    for distance in distances:
        radial = pnts + unit_vectors * distance
        rad_lines.append(radial)

    # make sure last point is the same as the first point
    hole_pnt_tags[-1] = hole_pnt_tags[0]
    FACTORY.synchronize()
    lines = [
        FACTORY.addLine(pnt, hole_pnt_tags[idx + 1])
        for idx, pnt in enumerate(hole_pnt_tags[:-1])
    ]
    hole = FACTORY.addCurveLoop(lines)
    return hole, hole_points, rad_lines
