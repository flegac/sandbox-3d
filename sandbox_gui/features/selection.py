from typing import Callable, Type

from direct.showbase.DirectObject import DirectObject
from panda3d.core import NodePath

type NodeUpdater = Callable[[NodePath], ...]


class Selection[T](DirectObject):
    def __init__(self, _type: Type[T], remove_condition: Callable[[T], bool] = None):
        self.remove_condition = remove_condition
        self.selection: set[T] = set()
        self.on_add: list[NodeUpdater] = []
        self.on_remove: list[NodeUpdater] = []

    @property
    def selected(self):
        if self.selection:
            return list(self.selection)[0]

    def select(self, selection: list[T]):
        self.clear()
        list(map(self.add, selection))
        for _ in selection:
            self.add(_)

    def remove(self, item: T):
        self.selection.remove(item)
        for _ in self.on_remove:
            _(item)

    def add(self, item: T):
        self.selection.add(item)
        for _ in self.on_add:
            _(item)

    def switch(self, item: T):
        if item in self.selection:
            self.remove(item)
        else:
            self.add(item)

    def clear(self):
        for _ in list(self.selection):
            self.remove(_)

    def keep_only(self):
        if self.remove_condition:
            for _ in filter(self.remove_condition, self.selection):
                self.selection.remove(_)

    def __contains__(self, item: T):
        self.keep_only()
        return item in self.selection

    def __iter__(self):
        self.keep_only()
        for _ in self.selection:
            yield _
