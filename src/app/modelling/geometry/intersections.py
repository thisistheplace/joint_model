"""Unfold a tube and and figure out where intersections are with other tubes

Process is:
- figure out which tube is main tube
- figure out where arc length to intersections
- unfold main tube and intersecting vectors
- calculate shape of intersection of plane and vector / tube (this should be an oval)
- create holes in planar surface
"""
from ...interfaces import *

class IntersectionError(Exception):
    pass

def intersections(master: NpTubular, slaves: list[NpTubular]) -> list[NpPoint3D]:
    """Calculate 3D points where slaves intersect master
    
    Args:
        master: 3D tubular with slave tubes may intersect
        slaves: list of 3D tubulars which may intersect master

    Returns:
        List of NpPoint3D where slaves intersect with master

    Raises:
        IntersectionError if any of the slaves don't intersect the master
    """
    
    pass

def flatten_tube():
    """Flattens """
    pass