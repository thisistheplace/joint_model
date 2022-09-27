from copy import deepcopy
import gmsh
import math
import numpy as np

from app.interfaces.numpy.model import NpTubular

from ..geometry.line import line_points
from .holes import hole_curve
from ..geometry.weld import get_weld_intersect_points
from ..geometry.intersections import flat_tube_intersection

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

    pnt_tags = [FACTORY.addPoint(*pnt.tolist()) for pnt in line_of_points]
    lines = [
        FACTORY.addLine(pnt, pnt_tags[idx + 1]) for idx, pnt in enumerate(pnt_tags[:-1])
    ]
    perimeter = FACTORY.addCurveLoop(lines)

    # get curves defining holes
    # TODO: check that slave names are unique!
    holes = []
    radial_lines = {}
    for slave in slaves:
        hole, rad_lines = hole_curve(master, slave)
        holes.append(hole)
        radial_lines[slave.name] = rad_lines

    # TODO: this bit!
    # Figure out if any radial lines are going to overlap with the holes.
    # Find max "radius" of each hole and radial lines.

    # Get centres
    centers = {}
    for slave in slaves:
        centers[slave.name] = flat_tube_intersection(map_to_np(master), map_to_np(slave))

    # Start biggest to smallest
    num_radials = len(list(radial_lines.values())[0])
    for idx in range(num_radials, 0, -1):
        line_idx = idx - 1
        for this, this_lines in radial_lines.items():
            this_line = this_lines[line_idx]
            # find distance to centers
            for other, other_lines in radial_lines.items():
                other_line = other_lines[line_idx]
                # reverse the order of other_lines to find intersect

                if this == other:
                    continue

                diff_center = (centers[this] + centers[other]) / 2.

                # check if slaves are too far away from each other for radials to intersect each other
                # TODO: make this more exact! bounding ellipse?
                this_center_distances = np.linalg.norm(this_line - centers[this], axis=1).max()
                this_diff_center_distances = np.linalg.norm(this_line - diff_center, axis=1).min()
                other_center_distances = np.linalg.norm(other_line - centers[other], axis=1).max()
                other_diff_center_distances = np.linalg.norm(other_line - diff_center, axis=1).min()

                if this_center_distances < this_diff_center_distances and other_center_distances < other_diff_center_distances:
                    continue

                this_diff_y_direction = np.sign(diff_center[0] - centers[this][0])
                other_diff_y_direction = np.sign(diff_center[0] - centers[other][0])

                this_diffs_y = diff_center[0] - this_line[:, 0]
                other_diffs_y = diff_center[0] - other_line[:, 0]

                this_diffs_y_sign = np.sign(this_diffs_y)
                other_diffs_y_sign = np.sign(other_diffs_y)

                this_no_change = this_diffs_y_sign == this_diff_y_direction
                other_no_change = other_diffs_y_sign == other_diff_y_direction

                this_average_y = this_line[:, 0] * this_no_change + diff_center[0] * (this_no_change == False)
                other_average_y = other_line[:, 0] * other_no_change + diff_center[0] * (other_no_change == False)

                radial_lines[this][line_idx][:, 0] = this_average_y
                radial_lines[other][line_idx][:, 0] = other_average_y

    # weld_pnts = []
    # for radials in radial_lines.values():
    #     for radial in radials:
    #         for pnt in radial:
    #             weld_pnts.append(pnt)
    # points = line_of_points + weld_pnts
    # x = [pnt[0] for pnt in points]
    # y = [pnt[1] for pnt in points]
    # z = [pnt[2] for pnt in points]
    # import plotly.express as px
    # fig = px.scatter_3d(x=x, y=y, z=z)
    # fig.show()

    # raise TypeError()

    # Create curves to apply mesh contraints at radial positions around holes
    mesh_constraints = []
    all_points = []
    for radials in radial_lines.values():
        for radial in radials:
            rad_pnt_tags = [FACTORY.addPoint(*pnt.tolist()) for pnt in radial]
            rad_pnt_tags.append(rad_pnt_tags[0])
            all_points += rad_pnt_tags
            rad_line = [
                FACTORY.addLine(pnt, rad_pnt_tags[idx + 1])
                for idx, pnt in enumerate(rad_pnt_tags[:-1])
            ]
            mesh_constraints.append(FACTORY.addCurveLoop(rad_line))

    FACTORY.synchronize()

    surface = FACTORY.addPlaneSurface([perimeter] + holes)
    FACTORY.synchronize()

    # Embed radial curves in surface so they become meshed
    gmsh.model.mesh.embed(1, mesh_constraints + holes, 2, surface)
    gmsh.model.mesh.embed(0, all_points, 2, surface)

    # We delete the source geometry, and increase the number of sub-edges for a
    # nicer display of the geometry:
    for l in lines:
        FACTORY.remove([(1, l)])
    FACTORY.remove([(1, perimeter)])
    FACTORY.synchronize()
    # gmsh.option.setNumber("Geometry.NumSubEdges", 20)
    return [2, surface]