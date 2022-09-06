import dash_vtk


def vtk_to_dash(data: dict[str, list]) -> dash_vtk.PolyData:
    return dash_vtk.PolyData(
        points=data["points"],
        lines=data["lines"],
        polys=data["polys"],
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
