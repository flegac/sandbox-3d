from dataclasses import dataclass

from panda3d.core import NodePath

from sandbox_core.entity.entity import EntityNode
from procedural_gen.region.vec import Vec


@dataclass
class RayCollision:
    entity: EntityNode
    node: NodePath
    pos: Vec
    normal: Vec
