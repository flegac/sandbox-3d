from pathlib import Path

from sandbox_creature.gesture.gesture import Gesture
from sandbox_creature.gesture.gesture_loader import GestureLoader
from sandbox_creature.core.skeleton import Skeleton


class GestureSwitcher:

    @staticmethod
    def from_path(skeleton: Skeleton, path: Path):
        loader = GestureLoader(skeleton, path)
        return GestureSwitcher([
            loader.load(_.name)
            for _ in path.iterdir()
            if _.is_file()
            if _.suffix == '.json'

        ])

    def __init__(self, gestures: list[Gesture]):
        self.gestures = gestures
        self.current = 0

    def next(self):
        self.gestures[self.current].run()
        self.current += 1
        self.current %= len(self.gestures)
