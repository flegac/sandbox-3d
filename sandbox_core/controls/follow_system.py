from typing import override

from python_ecs.system import System
from sandbox_core.controls.follow import Follow


class FollowSystem(System):
    _signature = Follow

    @override
    def update_single(self, follow: Follow):
        follow._origin.setPos(follow._target.get_pos())
