from typing import override

from sandbox_creature.behavior.behavior import Behavior


class ComplexBehavior(Behavior):
    _sates: list[Behavior]

    @staticmethod
    def from_states(states: list[Behavior]):
        res = ComplexBehavior()
        res._states = states
        return res

    @override
    def update(self):
        for state in self._states:
            if state.match():
                return state.update()
