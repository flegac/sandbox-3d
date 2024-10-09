from functools import cached_property
from pathlib import Path

from easy_kit.timing import time_func, timing
from procedural_gen.region.vec import Vec
from python_ecs.ecs import sim
from python_ecs.storage.database import Database
from python_ecs.system import System
from sandbox_core.physics.rigid_body import RigidBody
from sandbox_core.transform import ETransform
from sandbox_lib.terrain.terrain_area import TerrainArea
from sandbox_lib.terrain.tiling import Coord, Tiling


class TerrainSystem(System):
    _signature = TerrainArea

    data_root: Path
    avatar: RigidBody = None
    max_elevation: float = 3
    last_coord: Coord | None = None

    @cached_property
    def grid(self):
        return Tiling[TerrainArea](64)

    def get_elevation(self, pos: Vec):
        terrain = self.grid.get(pos)
        return terrain.get_elevation(pos)

    def update(self, db: Database, dt: float):
        avatar = self.avatar
        new_pos = avatar.pos

        new_coord = self.grid.to_coord(new_pos)
        if new_coord != self.last_coord:
            with timing('Terrain.update_grid_cells'):
                with timing('Terrain.update_grid_cells.prepare'):
                    last_area = self.grid.cells(self.last_coord)
                    new_area = self.grid.cells(new_coord)
                    to_create = new_area.difference(last_area)
                    to_delete = last_area.difference(new_area)
                with timing(f'Terrain.update_grid_cells.destroy[{len(to_delete)}]'):
                    for coord in to_delete:
                        self.destroy(coord)
                with timing(f'Terrain.update_grid_cells.create[{len(to_create)}]'):
                    for coord in to_create:
                        self.create(coord)
                self.last_coord = new_coord
        else:
            last_area = self.grid.cells(self.last_coord)
            for item in last_area:
                terrain = self.grid.get(item)
                terrain.entity.display.model.terrain.setFocalPoint(avatar.node)
                terrain.entity.display.model.terrain.update()

    @time_func
    def destroy(self, coord: Coord):
        terrain = self.grid.get(coord)
        if terrain:
            sim.destroy([
                terrain.entity.eid,
                *[_.eid for _ in terrain.vegetation],
            ])

    @time_func
    def create(self, coord: Coord):

        if coord not in self.grid:
            terrain = TerrainArea(
                path=self.data_root / 'tile',
                transform=ETransform(
                    position=self.grid.to_vec(coord),
                    scale=Vec.at(self.grid.size, self.grid.size, self.max_elevation)
                ),
            )
            self.grid.create(coord, terrain)
        terrain = self.grid.get(coord)
        terrain.entity.new_entity()

        for _ in terrain.vegetation:
            _.new_entity()
