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
    for idx, pnt in enumerate(
        get_weld_intersect_points(npmaster, npslave, angle_inc=angle)
    ):
        hole_pnt_tags.append(FACTORY.addPoint(*pnt.tolist()))
        pnts[idx, :] = pnt

    flat_intersect = flat_tube_intersection(npmaster, npslave)

    # Vectors from center points to points
    vectors = flat_intersect - pnts
    unit_vectors = (vectors.T / np.linalg.norm(vectors, axis=1)).T

    # create points at radial distances away from hole points
    distances = [0.1, 0.2, 0.3, 0.4]
    # distances = [0.2]
    rad_lines = []
    for distance in distances:
        radial = flat_intersect + unit_vectors * distance
        # rad_pnt_tags = [FACTORY.addPoint(*pnt.tolist()) for pnt in radial]
        # rad_pnt_tags[-1] = rad_pnt_tags[0]
        # rad_line = [
        #     FACTORY.addLine(pnt, rad_pnt_tags[idx + 1])
        #     for idx, pnt in enumerate(rad_pnt_tags[:-1])
        # ]
        # rad_lines.append(FACTORY.addCurveLoop(rad_line))
        rad_lines.append(radial)

    # make sure last point is the same as the first point
    hole_pnt_tags[-1] = hole_pnt_tags[0]
    FACTORY.synchronize()
    lines = [
        FACTORY.addLine(pnt, hole_pnt_tags[idx + 1])
        for idx, pnt in enumerate(hole_pnt_tags[:-1])
    ]
    hole = FACTORY.addCurveLoop(lines)
    # Delete the source geometry for a nicer display of the geometry:
    for l in lines:
        FACTORY.remove([(1, l)])
    return hole, rad_lines
