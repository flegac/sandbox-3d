import inspect
from collections.abc import Callable, Mapping, Iterable, Sequence
from typing import Any

from panda3d.core import NodePath
from pydantic import BaseModel

from sandbox_core.events.event_config import EventConfig
from sandbox_core.physics.rigid_body import RigidBody
from procedural_gen.region.vec import Vec


def to_gui(data: Any):
    match data:
        case NodePath():
            return f'({type(data).__name__}){to_gui({
                'name': data.name,
                'xyz': data.get_pos(),
                'hpr': data.get_hpr(),
                'scale': data.getScale(),
            })}'
        case RigidBody():
            return to_gui({
                'pos': data.pos,
                'hpr': data.hpr,
                'speed': data.linear_velocity,
                'angular': data.angular_velocity,
                'mass': data.mass,
            })
        case EventConfig():
            return f'{type_label(data)}\n{to_gui(data.mapping)}'
        case Vec():
            return f'{data}'
        # python types
        case float():
            return f'{data:.1f}'
        case str() | tuple() | int() | None:
            return f'{data}'
        case Mapping():
            return '\n'.join([
                f'  {k}: {to_gui(v)}'
                for k, v in data.items()
            ])
        case Callable():
            if inspect.ismethod(data):
                return f'{data.__self__.__class__.__name__}.{data.__name__}'
            return f'{data.__qualname__}'
        case Sequence() | Iterable():
            return f'{'\n'.join(list(map(to_gui, data)))}'

        # generic types
        case BaseModel():
            return f'{type_label(data)}{data}'

        case _:
            try:
                return to_gui(Vec.cast(data))
            except:
                return f'?{type_label(data)}{data}'


def type_label(item: Any):
    return f'({type(item).__name__})'
