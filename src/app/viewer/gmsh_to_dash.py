import dash_vtk

from ..interfaces import DashVtkModel


def vtk_to_dash(model: DashVtkModel) -> dash_vtk.PolyData:
    return dash_vtk.PolyData(
        points=model.mesh.points,
        lines=model.mesh.lines,
        polys=model.mesh.polys,
        children=[
            dash_vtk.PointData(
                [
                    dash_vtk.DataArray(
                        # registration='setScalars', # To activate field
                        name="onPoints",
                        values=[0, 0.33, 0.66, 1],
                    )
                ]
            ),
            dash_vtk.CellData(
                [
                    dash_vtk.DataArray(
                        # registration='setScalars', # To activate field
                        name="onCells",
                        values=[0, 1],
                    )
                ]
            ),
        ],
    )
