from abc import abstractmethod

from loguru import logger

from easy_kit.timing import time_func
from sandbox_creature.core.skeleton import Skeleton
from sandbox_creature.gesture.animation import Animation


class Gesture:
    def __init__(self, skeleton: Skeleton):
        self.skeleton = skeleton

    @time_func
    def run(self):
        logger.info(f'posture: {self}')
        seq = self.compute_sequence()
        for query, sequence in seq.iter():
            for joint in self.skeleton.search_joint(query):
                joint.sequence = sequence.clone()

        for name, value in seq.params.items():
            self.skeleton.config.params[name].set_value(value)

    @abstractmethod
    def compute_sequence(self) -> Animation:
        ...
