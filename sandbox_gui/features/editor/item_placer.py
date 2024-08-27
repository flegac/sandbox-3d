import random

from easy_kit.timing import time_func
from python_ecs.ecs import sim
from sandbox_core.display.display import Display
from sandbox_core.entity.entity import EntityNode
from sandbox_core.transform import ETransform
from sandbox_gui.features.editor.model_library import ModelLibrary
from procedural_gen.object_distribution.item_map import ItemMap
from procedural_gen.object_distribution.object_instance import ObjectInstance
from procedural_gen.region.region import Region
from procedural_gen.region.vec import Vec


class ItemPlacer:
    def __init__(self, library: ModelLibrary):
        self.library = library
        self.item_map = ItemMap()

        self.models = self.library.models
        for _ in self.models:
            _.model_node().set_hpr(0, 90, 0)

    def reset(self):
        self.item_map.mask.reset()
        return self

    @time_func
    def create_all(self, n: int, radius: float = 1, region: Region = None):
        if region is None:
            region = Region.from_center(Vec(), radius=128)
        assert region.x.size == region.y.size
        region_size = region.x.size

        items = self.item_map.place_items(
            ObjectInstance(object_id=0, radius=radius / region_size),
            n=n
        )

        models = []
        for item in items:
            model = random.choice(self.models)
            scaling = model.get_scaling(2 * radius)
            models.append(self.place_item(Display(
                model=model,
                is_instance=True,
                transform=ETransform(
                    position=self.get_pos(item, region),
                    scale=Vec.cast(scaling)
                )
            )))

        return models

    def get_pos(self, item: ObjectInstance, region: Region):
        from sandbox_lib.terrain.terrain_system import TerrainSystem

        region_size = region.x.size
        offset = Vec.at(region.start.x, region.start.y)
        pos = offset + Vec.at(item.position.x, item.position.y, 0) * region_size

        terrain = sim.find(TerrainSystem)
        pos.z = terrain.get_elevation(pos)
        return pos

    def place_item(self, display: Display):
        return EntityNode(
            display=display,
        )

        # return EntityNode(
        #     display=display,
        #     phys=RigidBody(
        #         transform=ETransform(
        #             position=pos,
        #             rotation=Vec.x_axis() * random.random() * 360
        #         ),
        #         is_ghost=True,
        #         shape=BoxShape()
        #     )
        # )
