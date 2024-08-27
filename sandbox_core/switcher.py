from sandbox.my_base import base
from sandbox_core.switchable import Switchable
from sandbox_core.unique_id import UniqueId


class Switcher[T](Switchable):
    def __init__(self, _type: type[T]):
        super().__init__()
        self.items: list[T] = []

    @property
    def name(self):
        return f'{self.__class__.__name__}-{UniqueId.next()}'

    def register(self, *items: T):
        for item in items:
            self.items.append(item)

    def _enable(self):
        for _ in self.items:
            _.switch(True)

    def _disable(self):
        base.task_mgr.remove(self.name)
        for _ in self.items:
            _.switch(False)
