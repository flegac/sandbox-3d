from typing import Callable

from python_ecs.component import Component


class ParamUpdater(Component):
    updater: Callable[[float], ...]

    def __call__(self, value: float):
        return self.updater(value)
