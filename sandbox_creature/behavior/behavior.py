from abc import abstractmethod
from functools import cached_property

from python_ecs.component import Component
from sandbox_creature.behavior.skeleton_physics import SkeletonPhysics
from sandbox_creature.core.skeleton import Skeleton


class Behavior(Component):
    skeleton: Skeleton | None = None

    @cached_property
    def extra(self):
        return SkeletonPhysics(self.skeleton)

    def match(self) -> bool:
        return True

    @abstractmethod
    def update(self):
        pass

    @property
    def type_id(self):
        return Behavior
