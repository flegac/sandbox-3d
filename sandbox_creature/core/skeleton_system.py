from typing import override

from python_ecs.storage.database_api import DatabaseAPI
from python_ecs.system import System
from sandbox_creature.core.skeleton import Skeleton


class SkeletonSystem(System):
    _signature = Skeleton

    @override
    def register(self, item: Skeleton):
        # for bone in item.bone_map.values():
        #     bone.create()

        for joint in item.joint_map.values():
            joint.create()

    @override
    def update_single(self, db: DatabaseAPI, item: Skeleton, dt: float):
        for name, param in item.config.params.items():
            param.play_sequence()

        for joint in item.joint_map.values():
            joint.update()
