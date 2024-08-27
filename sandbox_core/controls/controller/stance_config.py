from collections import defaultdict

from pydantic import Field

from easy_config.my_model import MyModel
from easy_kit.timing import time_func
from sandbox_core.controls.params.float_param import FloatParam
from sandbox_core.controls.params.vec_param import VecParam
from procedural_gen.region.vec import Vec


class StanceConfig(MyModel):
    params: dict[str, FloatParam] = Field(default_factory=lambda: defaultdict(FloatParam))

    @time_func
    def update(self):
        for name, param in self.params.items():
            param.update()

    def reset(self):
        for name, param in self.params.items():
            param.reset()

    def normalized(self, name: str):
        param = self.params[name]
        value = param.current
        if value > 0:
            return value / abs(param.high)
        if value < 0:
            return value / abs(param.low)
        return 0

    @time_func
    def float(self, name: str, default: float = None) -> float:
        param = self.params[name]
        if param.current is None:
            return default
        return param.current

    def vec(self, name: str):
        return Vec.at(
            self.float(f'{name}.x', 0),
            self.float(f'{name}.y', 0),
            self.float(f'{name}.z', 0),
        )

    def with_param(self, name: str, param: FloatParam):
        self.params[name] = param
        return self

    def with_vec(self, name: str, param: VecParam):
        self.with_param(f'{name}.x', param.project(0))
        self.with_param(f'{name}.y', param.project(1))
        self.with_param(f'{name}.z', param.project(2))
        return self
