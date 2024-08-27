import math
import random
from pathlib import Path

from direct.showbase.ShowBaseGlobal import globalClock, base

from python_ecs.component import Component
from sandbox_core._utils.ray.physic_ray import RayCollision
from sandbox_core.display.display import Display
from sandbox_core.display.geometry_model import GeometryModel
from sandbox_core.entity.entity import EntityNode
from sandbox_core.entity.health import Health
from sandbox_core.entity.lifetime import Lifetime
from sandbox_core.physics.rigid_body import RigidBody
from sandbox_core.physics.shapes.sphere_shape import SphereShape
from sandbox_core.transform import ETransform
from procedural_gen.region.vec import Vec
from sandbox_gui.features.panels.sound_panel import MUSIC_ROOT

PROJECTILE_RADIUS = .1



def make_projectile():
    projectile = EntityNode(
        lifetime=Lifetime(lifetime=1.5),
        health=Health(
            hit_damage=250,
        ),
        display=Display(
            model=GeometryModel(geometry_path=Path('shapes/icosahedron.egg')),
            transform=ETransform(
                scale=Vec.cast(PROJECTILE_RADIUS / math.pi)
            )
        ),
        phys=RigidBody(
            density=100,
            friction=0,
            restitution=5,
            angular_damping=0,
            linear_damping=0,
        ),
    )
    projectile.phys.shape = SphereShape(radius=PROJECTILE_RADIUS)
    projectile.new_entity()
    return projectile


class ShooterConfig(Component):
    origin: RigidBody
    transform: ETransform

    rate_of_fire: float = .07
    projectile_speed: float = 50
    dispersion: float = .01
    fire_sum: float = 0
    is_firing: bool = False

    @staticmethod
    def handler(shooters: list['ShooterConfig']):
        def shoot(status: bool):
            for shooter in shooters:
                shooter.is_firing = status

        return shoot

    def is_unavailable(self):
        dt = globalClock.getDt()

        self.fire_sum += dt
        if self.fire_sum < self.rate_of_fire:
            return True
        self.fire_sum -= self.rate_of_fire
        return False

    def shoot_at(self, item: RayCollision):
        origin = self.origin.pos + self.transform.position

        # Create bullet
        projectile = make_projectile()
        projectile.phys.body.set_ccd_motion_threshold(1e-7)
        projectile.phys.body.set_ccd_swept_sphere_radius(projectile.phys.shape.radius)

        v = (item.pos - origin).normalized()
        v += Vec.rand_direction(self.dispersion)
        v *= self.projectile_speed + random.random() * self.projectile_speed / 2
        projectile.phys.linear_velocity += v
        projectile.phys.pos = origin

        item = random.choice('ABC')
        base.audio.play_sfx(
            # sound=f'{MUSIC_ROOT}/Cool/FX/Hollywood Action/Hollywood Action/Weapon/Rifle/Rifle Shot {item}.wav',
            sound=f'{MUSIC_ROOT}/Cool/FX/Medieval Fantasy/Medieval Fantasy/Weapons and Armor/Bow/Bow Arrow Fire {item}.wav',
            # sound=f'{MUSIC_ROOT}/Cool/FX/Sci-Fi/Sci-Fi/Weapon/Heavy/Proton Heavy Gun {item}.wav',
            target=self.origin.node,
        )
