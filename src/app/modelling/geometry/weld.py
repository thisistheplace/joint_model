import math
from math import cos, sin, sqrt

from .vectors import angle_between_vectors
from ...interfaces import *

# TODO: look into https://mathcurve.com/courbes2d.gb/alain/alain.shtml

def x(r1: float, r2: float, pheta: float) -> float:
    return -1 * \
        sqrt(-1 * (r2 ** 2) + (r2 ** 2) * (cos(pheta) ** 2)+ (r1 ** 2))

def y(r2: float, pheta: float) -> float:
    return r2 * sin(pheta)

def z(r1: float, r2: float, phi: float, pheta: float) -> float:
    return -1 * \
        (r2 * cos(pheta) - cos(phi) * sqrt(-1 * (r2 ** 2) + (r2 ** 2) * (cos(pheta) ** 2)+ (r1 ** 2))) / \
            sin(phi)


def get_weld_intersect_points():

    for degrees in range(0, 361, 10):
        angle = degrees * math.pi / 360
        