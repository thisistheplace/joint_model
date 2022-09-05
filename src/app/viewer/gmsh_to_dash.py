from lib2to3.pytree import Base
import dash_vtk
from pydantic import BaseModel
import numpy as np

POINTS = "POINTS"
CONNECTIVITY = "CONNECTIVITY"
CELL_TYPES = "CELL_TYPES"


def read_until(lines: list, until: str):
    lidx = 0
    while until not in lines[lidx]:
        lidx += 1
    return lines[:lidx]


def vtk_to_dash(data) -> dash_vtk.PolyData:
    return dash_vtk.PolyData(
        points=[
            0,0,0,
            1,0,0,
            0,1,0,
            1,1,0,
        ],
        lines=[3, 1, 3, 2],
        polys=[3, 0, 1, 2],
        children=[
            dash_vtk.PointData([
                dash_vtk.DataArray(
                    #registration='setScalars', # To activate field
                    name='onPoints',
                    values=[0, 0.33, 0.66, 1],
                )
            ]),
            dash_vtk.CellData([
                dash_vtk.DataArray(
                    # registration='setScalars', # To activate field
                    name='onCells',
                    values=[0, 1],
                )
            ])
        ],
    )