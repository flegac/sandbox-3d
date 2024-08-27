from collections.abc import MutableMapping

from pydantic import Field

from easy_config.my_model import MyModel
from sandbox_creature.gesture.joint_sequence import JointSequence
from procedural_gen.region.vec import Vec

type TimeVec = tuple[float, tuple[float, float, float]]
type TimeSequence = TimeVec | list[TimeVec]
type AnimDict = dict[str, TimeSequence | AnimDict]


class Animation(MyModel):
    joints: AnimDict = Field(default_factory=dict)
    params: dict[str, float] = Field(default_factory=dict)

    def explicit(self):
        return flatten(self.joints)

    def iter(self):
        for query, hpr in self.explicit().items():
            if not isinstance(hpr, list):
                hpr = [hpr]
            hpr = [(time, Vec.at(*vec)) for time, vec in hpr]
            yield query, JointSequence(hpr=hpr)


def flatten(dictionary, parent_key='', separator=' '):
    # https://stackoverflow.com/questions/6027558/flatten-nested-dictionaries-compressing-keys
    items = []
    for key, value in dictionary.items():
        new_key = parent_key + separator + key if parent_key else key
        if isinstance(value, MutableMapping):
            items.extend(flatten(value, new_key, separator=separator).items())
        else:
            items.append((new_key, value))
    return dict(items)
