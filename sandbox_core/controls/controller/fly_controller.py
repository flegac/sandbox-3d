from panda3d.core import Vec3

from sandbox_core.controls.controller.phys_controller import PhysicController
from procedural_gen.region.vec import Vec


class FlyController(PhysicController):
    target_altitude: float = 1

    def input_handler(self):
        self.reset()

        if self.is_set('forward'):
            self._force.x += self.power
        if self.is_set('reverse'):
            self._force.x -= self.power

        if self.is_set('right'):
            self._force.y += self.power
        if self.is_set('left'):
            self._force.y -= self.power

        if self.is_set('up'):
            self.target_altitude += 1
        if self.is_set('down'):
            self.target_altitude -= 1

        if self.is_set('turnRight'):
            self._torque.z -= self.power
        if self.is_set('turnLeft'):
            self._torque.z += self.power

    def force(self, ref: tuple[Vec, Vec, Vec]):
        delta = self.target_altitude - self.targets[0].pos.z
        speed = self.targets[0].linear_velocity
        delta = delta - speed.z * .5
        print(self.target_altitude, delta)
        self._force.z = delta * self.power

        forward, up, right = ref

        forward = forward * self._force.x
        right = right * self._force.y
        up = Vec3(0, 0, 1) * self._force.z

        return (forward + right + up)
