from typing import override

from python_ecs.storage.database_api import DatabaseAPI
from python_ecs.system import System
from sandbox_core.controls.follow import Follow


class FollowSystem(System):
    _signature = Follow

    @override
    def update_single(self, db: DatabaseAPI, follow: Follow, dt: float):
        follow._origin.setPos(follow._target.get_pos())
