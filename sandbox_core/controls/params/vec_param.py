from easy_config.my_model import MyModel
from sandbox_core.controls.params.float_param import FloatParam
from procedural_gen.region.vec import Vec


class VecParam(MyModel):
    value: Vec
    default: Vec
    target: Vec
    speed: Vec

    low: Vec
    high: Vec

    @staticmethod
    def create(value: Vec, default: Vec = None, low: Vec = None, high: Vec = None, speed: Vec = None):
        if default is None:
            default = Vec()
        if low is None:
            low = Vec.at(None, None, None)
        if high is None:
            high = Vec.at(None, None, None)
        if speed is None:
            speed = Vec.at(None, None, None)
        target = Vec.cast(None)
        return VecParam(value=value, default=default, target=target, low=low, high=high, speed=speed)

    def project(self, i: int):
        return FloatParam(
            current=self.value.vec[i],
            default=self.default.vec[i],
            low=self.low.vec[i],
            high=self.high.vec[i],
            max_speed=self.speed.vec[i]
        )
