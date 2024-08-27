from panda3d.core import GeomVertexData, GeomVertexFormat, Geom, GeomVertexWriter, GeomTriangles, GeomNode

from procedural_gen.region.region import Region


def make_region(region: Region):
    x1, x2 = region.x.start, region.x.end
    y1, y2 = region.y.start, region.y.end
    z1, z2 = region.z.start, region.z.end
    data = [
        [x1, y1, z1, ],
        [x1, y1, z2, ],
        [x1, y2, z1, ],
        [x1, y2, z2, ],
        [x2, y1, z1, ],
        [x2, y1, z2, ],
        [x2, y2, z1, ],
        [x2, y2, z2, ],
    ]

    vdata = GeomVertexData('name', GeomVertexFormat.getV3t2(), Geom.UHStatic)
    vdata.setNumRows(len(data))
    vertex = GeomVertexWriter(vdata, 'vertex')
    # normal = GeomVertexWriter(vdata, 'normal')
    texcoord = GeomVertexWriter(vdata, 'texcoord')
    for row in data:
        x, y, z = row
        vertex.addData3(x, y, z)
        # normal.addData3(xn, yn, zn)
        texcoord.addData2(row[0], row[2])
    faces = GeomTriangles(Geom.UHStatic)
    faces.addVertices(1, 2, 3)
    faces.addVertices(1, 2, 3)
    faces.close_primitive()

    geom = Geom(vdata)
    geom.addPrimitive(faces)
    node = GeomNode('region')
    node.addGeom(geom)
    return node
