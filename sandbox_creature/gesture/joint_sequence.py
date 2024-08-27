import time

from pydantic import Field

from easy_config.my_model import MyModel
from easy_kit.timing import time_func
from sandbox_core.controls.params.float_param import FloatParam
from procedural_gen.region.vec import Vec


class JointSequence(MyModel):
    #TODO: use that ?
    rx: FloatParam = Field(default_factory=FloatParam)
    ry: FloatParam = Field(default_factory=FloatParam)
    rz: FloatParam = Field(default_factory=FloatParam)

    hpr: list[tuple[float, Vec]] = Field(default_factory=list)

    _start: int | None = None
    _origin: Vec | None = None

    @property
    def total_duration(self):
        return sum([d for d, _ in self.hpr])

    @property
    def elapsed_sec(self):
        if self._start is None:
            return 0
        return (time.time_ns() - self._start) * 10 ** -9

    @property
    def is_done(self):
        if self._start is None:
            return False
        return self.elapsed_sec > self.total_duration

    @time_func
    def play(self, current: Vec):
        if self._start is None:
            self._start = time.time_ns()
            self._origin = current

        if self.is_done:
            return current

        x, target = self.find_next()
        return self.interpolate(current, target, x)

    def find_next(self):
        total = 0
        for duration, hpr in self.hpr:
            total += duration
            if self.elapsed_sec > total:
                self._origin = hpr
                continue
            x = 1 - (total - self.elapsed_sec) / duration
            return x, hpr
        return 0, None

    def interpolate(self, current: Vec | None, target: Vec | None, x: float):
        if x > 1:
            return target

        return Vec.interpolate(self._origin, target, x)
