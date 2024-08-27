from pathlib import Path

from loguru import logger

from easy_kit.timing import time_func
from sandbox.configgg import DATA_ROOT
from sandbox_core.assets.library import Query, Library
from sandbox_core.display.geometry_model import GeometryModel


class ModelLibrary:
    def __init__(self, query: Query, root: Path = None):
        self.root = root or DATA_ROOT / 'models'
        self.query = query
        self.model_paths: list[Path] = None
        self.models: list[GeometryModel] = None
        self.update_models()

    @time_func
    def models(self):
        return [self.get_model(_) for _ in self.model_paths]

    @staticmethod
    def get_model(model_path: Path):
        return GeometryModel(
            geometry_path=model_path,
            color_path=ModelLibrary._search_texture(model_path),
        )

    def update_models(self):
        self.model_paths = self.library.search(self.query)
        self.models = [self.get_model(_) for _ in self.model_paths]
        return self.model_paths

    @property
    def library(self):
        return Library(self.root)

    @staticmethod
    def _search_texture(path: Path):
        lookup = [
            path.parent.parent,
            path.parent.parent / 'Textures',
        ]

        for root in lookup:
            try:
                return next(root.glob(f'**/*.png'))
            except:
                logger.warning(f'no texture at {root}')
