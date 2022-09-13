import gmsh
import math
import numpy as np

from ...interfaces import *
from ..geometry.intersections import intersections, plane_intersect

FACTORY = gmsh.model.occ

def create_holes(master: NpTubular, slaves: list[NpTubular]) -> dict[str, np.ndarray]:
    """Create holes in current mesh based on tubular intersections
    
    Args:
        master: 3D tubular with slave tubes may intersect
        slaves: list of 3D tubulars which may intersect master

    Returns:
        Dict of np.ndarray where slaves intersect with master (key: NpTubular.name)

    Raises:
        IntersectionError if any of the slaves don't intersect the master
    """
    for k, point in intersections(master, slaves):
        pnt_tags = [FACTORY.addPoint(*pnt.tolist()) for pnt in line_of_points]
        lines = [FACTORY.addLine(pnt, pnt_tags[idx + 1]) for idx, pnt in enumerate(pnt_tags[:-1])]
        curve = FACTORY.addCurveLoop(lines)
    

def hole(point: np.ndarray, vector: np.ndarray, diameter: float, specs: MeshSpecs) -> list[np.array]:
    """Create a list of points defining the edge of a hole
    
    Args:
        point: intersection point of vector on X/Z plane
        vector: vector of circular tube intersecting plane
        diameter: diameter of hole
        specs: MeshSpecs to use in meshing

    Returns:
        List of points along line, first point is duplicated last (closed loop)
    """
    
