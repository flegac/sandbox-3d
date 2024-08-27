from panda3d.bullet import BulletTriangleMesh, BulletTriangleMeshShape, BulletBodyNode

from sandbox_core.physics.shapes.abstract_shape import AbstractShape


class MeshShape(AbstractShape):
    name: str = 'mesh'
    entity: 'EntityNode' = None

    def create(self, body: BulletBodyNode):
        for n in self.entity.display.model_node.findAllMatches('**/+GeomNode').getPaths():
            for geom in n.node().getGeoms():
                mesh = BulletTriangleMesh()
                mesh.addGeom(geom)
                body.add_shape(BulletTriangleMeshShape(mesh, dynamic=True))

    def volume(self):
        raise NotImplementedError
