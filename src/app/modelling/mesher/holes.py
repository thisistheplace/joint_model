import gmsh
import numpy as np

from ...interfaces import *
from ..geometry.intersections import intersections
from ..geometry.points import ellipse_quadrant_points

FACTORY = gmsh.model.occ


def create_holes(master: NpTubular, slaves: list[NpTubular], specs: MeshSpecs) -> dict[str, np.ndarray]:
    """Create holes in current mesh based on tubular intersections

    Args:
        master: 3D tubular with slave tubes may intersect
        slaves: list of 3D tubulars which may intersect master
        specs: MeshSpecs to configure meshing

    Returns:
        Dict of np.ndarray where slaves intersect with master (key: NpTubular.name)

    Raises:
        IntersectionError if any of the slaves don't intersect the master
    """
    slave_dict = {slave.name: slave for slave in slaves}
    intersects = intersections(master, slaves)
    # TODO: determine radii of ellipse at intersection
    for k, point in intersects.items():
        radius = slave_dict[k].diameter / 2.0
        pnt_tags = [FACTORY.addPoint(pnt[0], pnt[1], point[2]) for pnt in ellipse_quadrant_points(point, radius, size=specs.size)]
        lines = [
            FACTORY.addLine(pnt, pnt_tags[idx + 1])
            for idx, pnt in enumerate(pnt_tags[:-1])
        ]
        curve = FACTORY.addSpline(lines)
        FACTORY.synchronize()
        for l in lines:
            FACTORY.remove([(1, l)])

    return intersects