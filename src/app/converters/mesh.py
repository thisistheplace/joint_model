from collections import defaultdict
import gmsh

from ..interfaces import DashVtkMesh


def process_mesh(mesh: gmsh.model.mesh):
    elementType = mesh.getElementType("Quadrangle", 1)
    faceNodes = mesh.getElementFaceNodes(elementType, 4)

    faceTags, _ = mesh.getFaces(4, faceNodes)
    elementTags, _ = mesh.getElementsByType(elementType)

    faces2Elements = defaultdict(list)

    for i in range(len(faceTags)):
        faces2Elements[faceTags[i]].append(elementTags[i])

    return faces2Elements


def mesh_to_dash_vtk(mesh: gmsh.model.mesh) -> DashVtkMesh:
    face2el = process_mesh(mesh)

    outerfaces = [k for k in face2el.keys()]

    nid2pointidx = {}  # key: node number, value: index in points
    points = []
    lines = []
    polys = []

    for element in outerfaces:
        _, node_ids = mesh.getElement(element)
        if len(node_ids) != 4:
            raise TypeError()
        # if eltype != 2 or len(node_ids) != 3:
        #     continue
        line = [len(node_ids) + 1]
        poly = [len(node_ids)]
        for nid in node_ids:
            if nid not in nid2pointidx:
                coords, _ = mesh.getNode(nid)
                points += coords.tolist()
                nid2pointidx[nid] = int(len(points) / 3 - 1)
            line.append(nid2pointidx[nid])
            poly.append(nid2pointidx[nid])
        line.append(line[1])

        lines += line
        polys += poly

    return DashVtkMesh(points=points, lines=lines, polys=polys)
