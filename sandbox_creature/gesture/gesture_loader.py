from pathlib import Path

from loguru import logger

from sandbox_creature.gesture.file_gesture import FileGesture
from sandbox_creature.core.skeleton import Skeleton


class GestureLoader:
    def __init__(self, skeleton: Skeleton, root: Path):
        self.skeleton = skeleton
        self.root = root

    def load(self, path: Path | str):
        logger.info(f'loading: {path}')
        return FileGesture(self.skeleton, self.root / path)
