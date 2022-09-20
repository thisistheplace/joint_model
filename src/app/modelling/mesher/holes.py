import gmsh
import numpy as np

from ...interfaces import *
from ...interfaces.mapper import map_to_np
from ..geometry.weld import get_weld_intersect_points

FACTORY = gmsh.model.occ

def hole_curve(master: Tubular, slave: Tubular) -> dict[str, np.ndarray]:
    pnt_tags = [FACTORY.addPoint(*pnt.tolist()) for pnt in get_weld_intersect_points(map_to_np(master), map_to_np(slave))]
    FACTORY.synchronize()
    lines = [
        FACTORY.addLine(pnt, pnt_tags[idx + 1]) for idx, pnt in enumerate(pnt_tags[:-1])
    ]
    return FACTORY.addCurveLoop(lines)

def create_holes(master: NpTubular, slaves: list[NpTubular], surface: int, specs: MeshSpecs) -> dict[str, np.ndarray]:
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
    slave_holes = {}
    # TODO: determine radii of ellipse at intersection
    for slave in slaves:
        curve = hole_curve(master, slave)
        FACTORY.synchronize()
        slave_holes[slave.name] = curve
        gmsh.model.mesh.embed(1, [curve], 2, surface)
        # for l in lines:
        #     FACTORY.remove([(1, l)])

    return slave_holes