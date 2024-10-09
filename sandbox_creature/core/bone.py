from functools import cached_property

from pydantic import Field, model_validator

from sandbox_core.display.display import Display
from sandbox_core.entity.entity import EntityNode
from sandbox_core.entity.health import Health
from sandbox_core.physics.rigid_body import RigidBody
from sandbox_creature.core.anatomic import Anatomic
from sandbox_creature.core.anchor import Anchor
from procedural_gen.region.vec import Vec

DEFAULT_BONE = EntityNode(
    health=Health(
        health=None,
        hit_damage=10,
    ),
    phys=RigidBody(
        density=2_000,
        angular_damping=.5,
        linear_damping=.1,
        friction=1,
        restitution=0,
    )
)


class Bone(Anatomic):
    center: Vec = Field(default_factory=Vec)
    anchors: dict[str, Anchor] = Field(default_factory=dict)
    entity: EntityNode = Field(default_factory=DEFAULT_BONE.clone)

    is_hidden: bool = False

    @property
    def phys(self):
        return self.entity.phys

    def new_anchor(self, name: str, offset: Vec = None, axis: Vec = None):
        anchor = Anchor.create(name=name, offset=offset, axis=axis)
        anchor._bone = self
        self.anchors[name] = anchor
        return anchor

    @property
    def name(self):
        return f'{self.__class__.__name__}-{self.id}'

    def at(self, anchor: str) -> 'Anchor':
        return self.anchors[anchor]

    @cached_property
    def points(self):
        return [_.vec for _ in self.anchors.values()]

    @property
    def body(self):
        return self.phys.body

    @property
    def pos(self):
        return self.phys.pos

    @property
    def hpr(self):
        return self.phys.hpr

    def create(self):
        center, size = Vec.bbox([_.offset for _ in self.anchors.values()])
        self.center += center
        for _ in self.anchors.values():
            _.offset -= center

        self.phys.transform.position = self.center

        if not self.is_hidden:
            self.entity.display = Display.from_shape(self.phys.shape)

        self.entity.new_entity()

    @model_validator(mode='after')
    def check_anchors(self):
        for name, a in self.anchors.items():
            a._bone = self
            a.name = name
        return self