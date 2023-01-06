from buildable.buildable import Buildable
from buildable.house import House
from buildable.structure import Structure
from class_types.walker_types import WalkerTypes
from walkers.walker import Walker


class Prefet(Walker):
    def __init__(self, associated_building: Buildable):
        super().__init__(WalkerTypes.PREFET, associated_building, max_walk_distance=10, roads_only=True)

    def update(self):
        super().update()
        tiles = self.current_tile.get_adjacente_tiles(2)
        for tile in tiles:
            if tile.get_building():
                if isinstance(tile.get_building(), House) or isinstance(tile.get_building(), Structure):
                    tile.get_building().risk.reset_fire_risk()