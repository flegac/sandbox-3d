from direct.showbase.InputStateGlobal import inputState

from python_ecs.component import Component
from sandbox.my_base import base
from sandbox_core.controls.params.float_param import FloatParam


class AxisConfig(Component):
    name: str
    events_incr: list[str]
    events_decr: list[str]
    power: float = .25

    _is_event_initialized: bool = False

    def init_events(self, param: FloatParam):
        if self._is_event_initialized:
            return
        self._is_event_initialized = True
        for _ in self.events_incr:
            self.add_event(param, _, True)
        for _ in self.events_decr:
            self.add_event(param, _, False)

    def add_event(self, param: FloatParam, event: str, direction: bool):
        if event.startswith('wheel'):
            delta = 1 if direction else -1
            base.accept(event, lambda: param.add_speed(delta * self.power ** 2))

        if direction:
            inputState.watchWithModifiers(f'{self.name}+', f'{event}')
        else:
            inputState.watchWithModifiers(f'{self.name}-', f'{event}')
