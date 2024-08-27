from enum import Enum

from panda3d.bullet import XUp, YUp, ZUp

from procedural_gen.region.vec import Vec


class Axis(Enum):
    x = XUp
    y = YUp
    z = ZUp

    @staticmethod
    def major(vec: Vec):
        res = Axis.z
        if vec.x > vec.z:
            res = Axis.x
        if vec.y > vec.z:
            res = Axis.y
        if vec.x > vec.y:
            res = Axis.x
        return res

    @staticmethod
    def minor(vec: Vec):
        res = Axis.z
        if vec.x < vec.z:
            res = Axis.x
        if vec.y < vec.z:
            res = Axis.y
        if vec.x < vec.y:
            res = Axis.x
        return res

    def get_value(self, vec: Vec):
        match self:
            case Axis.x:
                return vec.x
            case Axis.y:
                return vec.y
            case Axis.z:
                return vec.z
            case _:
                raise ValueError

    def set_value(self, vec: Vec, value: float):
        match self:
            case Axis.x:
                vec.x = value
            case Axis.y:
                vec.y = value
            case Axis.z:
                vec.z = value
            case _:
                raise ValueError

    def add_value(self, vec: Vec, value: float):
        self.set_value(vec, self.get_value(vec) + value)

    def rotate(self):
        match self:
            case Axis.x:
                return Vec.at(90, 0, 0)
            case Axis.y:
                return Vec.at(0, 90, 0)
            case Axis.z:
                return Vec.at(0, 0, 0)
