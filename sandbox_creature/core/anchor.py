from panda3d.core import TransformState, Point3, Vec3
from pydantic import Field

from easy_config.my_model import MyModel
from procedural_gen.region.vec import Vec


class Anchor(MyModel):
    name: str = None
    offset: Vec = Field(default_factory=Vec)
    axis: Vec = Field(default_factory=Vec)
    _bone: 'Bone' = None

    @staticmethod
    def create(name: str, offset: Vec = None, axis: Vec = None):
        return Anchor(name=name, offset=offset or Vec(), axis=axis or Vec())

    @staticmethod
    def vertical(vec: Vec):
        return Anchor(vec=vec, axis=Vec.at(0, 0, 90))

    @property
    def vec(self):
        return self._bone.center + self.offset

    @property
    def body(self):
        return self._bone.body

    def transform_state(self, center: Vec):
        offset = center - self._bone.center
        axis = self.axis
        return TransformState.make_pos_hpr(Point3(*offset.vec), Vec3(*axis.vec))

    def __repr__(self):
        bone_name = 'None'
        if self._bone is not None:
            bone_name = self._bone.name
        return f'{self.name}@{bone_name}'

    def __str__(self):
        return repr(self)
