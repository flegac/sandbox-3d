from sandbox.configgg import GESTURE_ROOT
from sandbox_core.events.event_config import EventConfig
from sandbox_creature.core.skeleton import Skeleton
from sandbox_creature.gesture.file_gesture import FileGesture
from sandbox_creature.gesture.gesture_switcher import GestureSwitcher


class SkeletonHandler(EventConfig):
    def __init__(self, skeleton: Skeleton):

        bye = FileGesture(skeleton, GESTURE_ROOT / 'bye.json')
        wip = FileGesture(skeleton, GESTURE_ROOT / 'wip.json')

        stances = GestureSwitcher.from_path(skeleton, GESTURE_ROOT / 'stance')
        guards = GestureSwitcher.from_path(skeleton, GESTURE_ROOT / 'guard')
        attacks = GestureSwitcher.from_path(skeleton, GESTURE_ROOT / 'attack')

        super().__init__(
            mapping={
                '&': attacks.next,
                '"': stances.next,
                '\'': guards.next,
                '(': wip.run
            },
            actions={
                'z': lambda s: self.params('forward').add_value(+1),
                's': lambda s: self.params('forward').add_value(-1),

                'q': lambda s: self.params('foot_balance').add_value(-.1),
                'd': lambda s: self.params('foot_balance').add_value(.1),

                '-': lambda s: self.params('knee_flexion').add_value(+2),
                '+': lambda s: self.params('knee_flexion').add_value(-2),

                '1': lambda s: self.params('hips_opening.x').add_value(+1),
                '2': lambda s: self.params('hips_opening.x').add_value(-1),

                '4': lambda s: self.params('hips_opening.y').add_value(-1),
                '5': lambda s: self.params('hips_opening.y').add_value(+1),

                '7': lambda s: self.params('hips_opening.z').add_value(+1),
                '8': lambda s: self.params('hips_opening.z').add_value(-1),

                '0': lambda s: skeleton.config.reset(),

                'space': self.jump
            }
        )
        self._skeleton = skeleton

    @property
    def skeleton(self) -> Skeleton:
        return self._skeleton

    def params(self, name: str):
        return self.skeleton.config.params[name]

    def jump(self, status: bool):
        if status:
            self.params('knee_flexion').add_value(50)
        else:
            self.params('knee_flexion').set_value(0)
