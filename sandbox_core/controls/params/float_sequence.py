import time

from pydantic import Field

from easy_config.my_model import MyModel
from easy_kit.timing import time_func


class FloatSequence(MyModel):
    values: list[tuple[float, float]] = Field(default_factory=list)
    _start: int | None = None
    _origin: float | None = None

    @property
    def total_duration(self):
        return sum([d for d, _ in self.values])

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
    def compute_next(self, current: float):
        if self._start is None:
            self._start = time.time_ns()
            self._origin = current

        if self.is_done:
            return current

        x, target = self.find_next()
        return self.interpolate(current, target, x)

    def find_next(self):
        total = 0
        for duration, value in self.values:
            total += duration
            if self.elapsed_sec > total:
                self._origin = value
                continue
            x = 1 - (total - self.elapsed_sec) / duration
            return x, value
        return 0, None

    def interpolate(self, current: float | None, target: float | None, x: float):
        if x > 1:
            return target

        if target is None:
            return self._origin
        if self._origin is None:
            self._origin = 0
        return self._origin * (1 - x) + target * x
