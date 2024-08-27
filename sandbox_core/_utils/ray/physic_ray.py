from loguru import logger
from panda3d.core import NodePath, \
    LPoint3, Vec3, BitMask32

from easy_kit.timing import time_func
from python_ecs.ecs import sim
from sandbox.my_base import base
from sandbox_core._utils.mouse import Mouse
from sandbox_core.entity.entity import EntityNode
from sandbox_core.physics.phys_system import PhysSystem
from sandbox_core.physics.ray_collision import RayCollision
from sandbox_core.physics.rigid_body import RigidBody
from procedural_gen.region.vec import Vec


class PhysicRay:
    @staticmethod
    def physics():
        return sim.find(PhysSystem)

    @time_func
    def mouse_ray(self, target_group: int = None):
        origin = LPoint3()
        target = LPoint3()
        base.camLens.extrude(Mouse.position(), origin, target)
        origin = Vec.cast(base.render.get_relative_point(base.cam, origin))
        target = Vec.cast(base.render.get_relative_point(base.cam, target))

        return self.ray_collision(origin, target, target_group)

    @time_func
    def get_elevation(self, vec: Vec):
        collision = self.ray_collision(vec + 100 * Vec.z_axis(), vec - 100 * Vec.z_axis(), self.physics().groups.static)
        return vec.z - collision.pos.z

    @time_func
    def fix_z(self, vec: Vec, force: bool = True):
        elevation = self.get_elevation(vec)
        if elevation < 0 or force:
            return vec - Vec.z_axis() * elevation
        return vec

    def iter_collision(self, origin: Vec, target: Vec, target_group: int = None):
        if target_group is not None:
            hits = self.physics().world.ray_test_all(Vec3(*origin.vec), Vec3(*target.vec), BitMask32.bit(target_group))
        else:
            hits = self.physics().world.ray_test_all(Vec3(*origin.vec), Vec3(*target.vec))
        for hit in hits:
            yield self._create_collision(hit, target)

    def ray_collision(self, origin: Vec, target: Vec, target_group: int = None):
        physics = sim.find(PhysSystem)
        if target_group is not None:
            hit = physics.world.ray_test_closest(Vec3(*origin.vec), Vec3(*target.vec), BitMask32.bit(target_group))
        else:
            hit = physics.world.ray_test_closest(Vec3(*origin.vec), Vec3(*target.vec))
        return self._create_collision(hit, target)

    def get_body_elevation(self, body: RigidBody):
        collision = self.phys_collision(body, - 100 * Vec.z_axis(), self.physics().groups.static)
        return body.pos.z - collision.pos.z

    def fix_body_z(self, body: RigidBody, force: bool = True):
        elevation = self.get_body_elevation(body)
        if elevation < 0 or force:
            body.pos = body.pos - Vec.z_axis() * elevation
        return body

    def phys_collision(self, body: RigidBody, direction: Vec, target_group: int = None):
        origin = body.transform.transform_state()
        target = body.transform.clone(
            update={'position': body.transform.position + direction}).transform_state()

        if target_group is not None:
            hit = self.physics().world.sweep_test_closest(
                body.bullet_shape, origin, target,
                BitMask32.bit(target_group))
        else:
            hit = self.physics().world.sweep_test_closest(body.bullet_shape, origin, target)
        return self._create_collision(hit, body.transform.position + direction)

    def _create_collision(self, hit, target: Vec):
        body_node = hit.getNode()
        pos = hit.getHitPos()
        normal = hit.getHitNormal()
        entity: EntityNode = None
        node: NodePath = None
        if body_node:
            try:
                node = base.render.find(f'**/{body_node.getName()}')
                entity = node.get_python_tag('entity')
            except Exception as e:
                logger.error(f'{e}')
        else:
            pos = target
        return RayCollision(
            entity=entity,
            node=node,
            pos=Vec.cast(pos),
            normal=Vec.cast(normal)
        )
