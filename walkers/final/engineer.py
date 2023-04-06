from buildable.buildable import Buildable
from buildable.house import House
from buildable.structure import Structure
from class_types.walker_types import WalkerTypes
from walkers.walker import Walker
from game.id import ID_GEN



class Engineer(Walker):
    def __init__(self, associated_building: Buildable,player_id:int=0, id:int=0 ):
        super().__init__(WalkerTypes.ENGINEER, associated_building, max_walk_distance=10, roads_only=True)
        id_create = ID_GEN()
        self.id = id_create.id_gen()
    def update(self):
        super().update()
        tiles = self.current_tile.get_adjacente_tiles(2)
        for tile in tiles:
            if tile.get_building():
                if isinstance(tile.get_building(), House) or isinstance(tile.get_building(), Structure):
                    tile.get_building().risk.reset_dest_risk()