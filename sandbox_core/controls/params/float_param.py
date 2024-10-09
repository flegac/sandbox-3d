from pydantic import Field

from easy_kit.timing import time_func
from easy_raster.utils.float_utils import clamp_abs, clamp
from python_ecs.component import Component
from sandbox_core.controls.params.float_sequence import FloatSequence


class FloatParam(Component):
    current: float = 0
    default: float = 0
    target: float | None = None

    sequence: FloatSequence = Field(default_factory=FloatSequence)

    speed: float = 0
    accel: float = 0
    friction: float = .9

    max_speed: float = 10

    low: float | None = None
    high: float | None = None
    modulo: bool = False

    def reset(self):
        self.set_value(self.default)

    @time_func
    def play_sequence(self):
        if self.sequence.is_done:
            return
        next_value = self.sequence.compute_next(self.current)
        self.set_value(next_value)

    @time_func
    def update(self):
        self.speed *= self.friction
        self.current = self._fix_value(self.current)
        delta = 0
        if self.target is not None:
            self.target = self._fix_value(self.target)
            delta = self.target - self.current
        self.set_speed(self.speed + delta + self.accel)
        self.current = self._fix_value(self.current + self.speed)

    def set_speed(self, speed: float):
        self.speed = clamp_abs(speed, 0, self.max_speed)

    @time_func
    def _fix_value(self, value: float):
        if self.modulo:
            while value < self.low:
                value += self.interval_size
            while value > self.high:
                value -= self.interval_size
        else:
            value = clamp(value, self.low, self.high)
        return value

    def set_value(self, value: float):
        self.target = self._fix_value(value)

    def add_value(self, value: float):
        self.set_value(self.current + value)

    def add_speed(self, delta: float):
        self.speed = clamp_abs(self.speed + delta, 0, self.max_speed)

    @property
    def interval_size(self):
        return abs(self.high - self.low)
