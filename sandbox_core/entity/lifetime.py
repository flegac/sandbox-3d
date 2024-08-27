import time

from python_ecs.component import Component


class Lifetime(Component):
    lifetime: float | None = None
    birth: float | None = None

    def reset(self):
        self.birth = time.time()

    @property
    def is_dead(self):
        if self.lifetime is None:
            return False
        if self.birth is None:
            self.reset()
        return time.time() > self.birth + self.lifetime
