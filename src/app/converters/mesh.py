from collections import defaultdict
import gmsh

from ..mesher.mesh import mesh_joint

def process_mesh(mesh: gmsh.model.mesh):
    # Like elements, mesh edges and faces are described by (an ordered list of)
    # their nodes. Let us retrieve the edges and the (triangular) faces of all the
    # first order tetrahedra in the mesh:
    elementType = mesh.getElementType("tetrahedron", 1)
    # edgeNodes = mesh.getElementEdgeNodes(elementType)
    faceNodes = mesh.getElementFaceNodes(elementType, 3)

    # Edges and faces are returned for each element as a list of nodes corresponding
    # to the canonical orientation of the edges and faces for a given element type.
    # Edge and face tags can then be retrieved by providing their nodes:
    # edgeTags, edgeOrientations = mesh.getEdges(edgeNodes)
    faceTags, faceOrientations = mesh.getFaces(3, faceNodes)
    elementTags, elementNodeTags = mesh.getElementsByType(elementType)

    # edges2Elements = defaultdict(list)
    faces2Elements = defaultdict(list)

    # for i in range(len(edgeTags)): # 6 edges per tetrahedron
    #     edges2Elements[edgeTags[i]].append(elementTags[i // 6])
    for i in range(len(faceTags)): # 4 faces per tetrahedron
        faces2Elements[faceTags[i]].append(elementTags[i // 4])

    return faces2Elements

def mesh_to_dash_vtk(mesh: gmsh.model.mesh):
    face2el = process_mesh(mesh)
    
    outerfaces = [k for k, v in face2el.items() if len(v) == 1]

    nid2pointidx = {} # key: node number, value: index in points
    points = []
    lines = []
    polys = []
    for element in outerfaces:
        eltype, node_ids = mesh.getElement(element)
        if eltype != 2:
            continue
        line = [3]
        poly = []
        for nid in node_ids:
            if nid not in nid2pointidx:
                coords, _ = mesh.getNode(nid)
                points += coords.tolist()
                nid2pointidx[nid] = len(points) / 3 - 1
            line.append(nid2pointidx[nid])
            poly.append(nid2pointidx[nid])
        poly.append(poly[0])

        lines += line
        polys += poly

    return {
        "points": points,
        "lines": lines,
        "polys": polys
    }