from functools import cached_property
from typing import Self

from pydantic import Field

from easy_config.my_model import MyModel
from easy_kit.timing import time_func
from sandbox_core.unique_id import UniqueId
from sandbox_creature.core.symmetry import Symmetry

TAG_SPLITTER = ' '


class Anatomic(MyModel):
    id: int | None = Field(default_factory=UniqueId.next)
    tags: str | None = Field(default_factory=set)
    symmetry: Symmetry | None = Field(default=Symmetry.default)

    @cached_property
    def tag_set(self):
        return set(map(str, self.tags.split(TAG_SPLITTER)))

    @staticmethod
    def parse(query: str):
        return Anatomic(tags=query)

    @property
    def qstring(self):
        tags = list(sorted(self.tags))
        return TAG_SPLITTER.join(tags)

    @time_func
    def match(self, item: Self):
        if item is None:
            return False
        with_id = self.id is None or self.id == item.id
        with_tags = self.tags is None or self.tag_set.issubset(item.tag_set)
        return all([with_tags])

    @time_func
    def search(self, skeleton: 'Skeleton', bones: bool = True, joints: bool = True):
        res = {}
        if bones:
            for _ in skeleton.bone_map.values():
                if self.match(_):
                    res[_.id] = _
        if joints:
            for _ in skeleton.joint_map.values():
                if self.match(_):
                    res[_.id] = _
        return list(res.values())

    def single(self, skeleton: 'Skeleton', bones: bool = True, joints: bool = True):
        found = self.search(skeleton, bones=bones, joints=joints)
        if len(found) != 1:
            raise ValueError(f'{self} found elements: {len(found)} {found}')
        return found[0]
