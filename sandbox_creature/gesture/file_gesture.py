from pathlib import Path

from loguru import logger

from easy_config.config import Config
from sandbox_creature.gesture.animation import Animation
from sandbox_creature.gesture.gesture import Gesture
from sandbox_creature.core.skeleton import Skeleton


class FileGesture(Gesture):

    def __init__(self, skeleton: Skeleton, path: Path):
        super().__init__(skeleton)
        self.path = path
        Config.read(self.path, Animation)

    def compute_sequence(self) -> Animation:
        try:
            return Config.read(self.path, Animation)
        except Exception as e:
            logger.error(f'{self.path}: {e}')
            return Animation()

    def __repr__(self):
        return f'Gesture({self.path.name})'

    def __str__(self):
        return repr(self)
