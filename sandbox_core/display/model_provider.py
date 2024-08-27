from abc import abstractmethod
from pathlib import Path

from panda3d.core import NodePath, TextureStage, SamplerState

from easy_config.my_model import MyModel
from sandbox.my_base import base


class ModelProvider(MyModel):
    color_path: Path | None = None
    color_scale: float = 1
    normal_path: Path | None = None

    @abstractmethod
    def model_node(self) -> NodePath:
        ...

    def update(self, node: NodePath):
        if self.color_path and self.color_path.exists():
            default_stage = TextureStage.getDefault()
            texture = base.loader.load_texture(self.color_path)
            texture.set_minfilter(SamplerState.FT_linear_mipmap_linear)
            texture.set_anisotropic_degree(1)
            node.set_texture(default_stage, texture)
            node.setTexScale(default_stage, self.color_scale)

        if self.normal_path and self.normal_path.exists():
            normal_stage = TextureStage('normal')
            normal_stage.setMode(TextureStage.MNormal)
            texture = base.loader.load_texture(self.normal_path)
            node.set_texture(normal_stage, texture)
