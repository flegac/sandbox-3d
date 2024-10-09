from functools import cached_property
from typing import Callable, Any, NewType

from direct.showbase.DirectObject import DirectObject
from direct.showbase.InputStateGlobal import inputState
from loguru import logger
from pydantic import Field, model_validator

from python_ecs.component import Component
from python_ecs.ecs import sim

Event = NewType('Event', str)
Status = NewType('Status', str)


class EventConfig(Component):
    # basic Event->Handler mapping
    mapping: dict[Event, Callable] = Field(default_factory=dict)

    # updaters: execute IF is_set(Status)
    actions: dict[Status, Callable[[bool], Any]] = Field(default_factory=dict)

    # Event -> Status switcher
    status_binding: dict[Status, Event] = Field(default_factory=dict)

    is_enabled: bool = False

    @cached_property
    def direct(self):
        return DirectObject()

    def is_set(self, name: str):
        return inputState.is_set(name)

    @model_validator(mode='after')
    def post_init(self):
        key_bindings = {
            **self.status_binding,
            **{x: x for x in self.actions}
        }

        for k, v in key_bindings.items():
            inputState.watchWithModifiers(k, v)

        for event, callback in self.mapping.items():
            self.direct.accept(event, callback)
        self.is_enabled = True
        logger.info(f'enable: {self}')

        sim.create_all([self])
        return self

    def __repr__(self):
        return f'{self.__class__.__name__}(enabled: {self.is_enabled}, {set(self.mapping.keys())}, actions: {set(self.actions.keys())})'

    def __str__(self):
        return repr(self)

    @property
    def type_id(self):
        return EventConfig
