from panda3d.core import Fog, NodePath

from easy_config.my_model import MyModel


class FogConfig(MyModel):
    name: str = 'fog'
    darkness: float = .0
    transparency: float = 400

    @property
    def exp_density(self):
        return 1 / self.transparency


class MyFog:
    def __init__(self, config: FogConfig = None):
        self.config = config or FogConfig()
        self.fog = Fog(self.config.name)
        darkness = self.config.darkness
        self.fog.setColor(darkness, darkness, darkness)
        self.fog.setExpDensity(self.config.exp_density)

    def apply(self, node: NodePath):
        node.setFog(self.fog)
