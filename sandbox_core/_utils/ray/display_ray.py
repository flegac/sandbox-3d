from loguru import logger
from panda3d.core import CollisionNode, GeomNode, CollisionRay, CollisionHandlerQueue, CollisionTraverser, NodePath, \
    CollisionEntry

from easy_kit.timing import time_func
from sandbox.my_base import base
from sandbox_core._utils.mouse import Mouse
from sandbox_core.physics.ray_collision import RayCollision
from procedural_gen.region.vec import Vec


class DisplayRay:
    def __init__(self):
        self.origin = base.render
        picker_node = CollisionNode(f'ray')
        picker_node.set_from_collide_mask(GeomNode.get_default_collide_mask())
        self.picker_ray = CollisionRay()
        picker_node.add_solid(self.picker_ray)
        picker_np = base.camera.attach_new_node(picker_node)

        self.queue = CollisionHandlerQueue()
        self.traverser = CollisionTraverser('traverser')
        self.traverser.add_collider(picker_np, self.queue)

    @time_func
    def launch(self):
        self.picker_ray.setFromLens(base.camNode, *Mouse.position())
        self.traverser.traverse(self.origin)
        if self.queue.getNumEntries() == 0:
            return
        self.queue.sortEntries()
        picked: CollisionEntry = self.queue.getEntry(0)
        node: NodePath = picked.getIntoNodePath()
        pos = picked.get_surface_point(self.origin)
        normal = picked.get_surface_normal(self.origin)
        logger.debug(node, pos, normal)
        return RayCollision(entity=None, node=node, pos=Vec.cast(pos), normal=Vec.cast(normal))
