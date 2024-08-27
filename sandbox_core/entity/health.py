from python_ecs.component import Component


class Health(Component):
    health: float | None = None
    hit_damage: float = 0.0

    def is_destructible(self):
        return self.health is not None

    @property
    def is_dead(self):
        if self.health is None:
            return False
        return self.health < 0
