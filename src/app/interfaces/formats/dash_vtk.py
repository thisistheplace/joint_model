from pydantic import BaseModel


class DashVtkMesh(BaseModel):
    # Flat list of 3D nodal coordinates
    # [x1, y1, z1, x2, y2, z2, ..., zN]
    points: list[float] = ...
    # List of number of nodes, and node indices defining polys
    # [N3, a, b, c, N2, aa, bb, N4, aaa, bbb, ccc, ddd, ...]
    polys: list[int] = ...
    # List of number of nodes, and node indices defining lines
    # [N3, a, b, c, N2, aa, bb, N4, aaa, bbb, ccc, ddd, ...]
    lines: list[int]


class DashVtkModel(BaseModel):
    name: str = ...
    mesh: DashVtkMesh = ...