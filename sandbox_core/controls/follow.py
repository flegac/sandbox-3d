from panda3d.core import NodePath

from python_ecs.component import Component


class Follow(Component):
    _origin: NodePath = None
    _target: NodePath = None

    @staticmethod
    def create(origin: NodePath, target: NodePath):
        res = Follow()
        res._origin = origin
        res._target = target
        return res
