from buildable.buildable import Buildable
from class_types.buildind_types import BuildingTypes
from buildable.house import House
from buildable.structure import Structure
from class_types.walker_types import WalkerTypes
from walkers.walker import Walker
from game.textures import Textures


class Granary_worker(Walker):
    def __init__(self, associated_building: Buildable):
        super().__init__(WalkerTypes.GRANARY_WORKER, associated_building, roads_only=True)

    def go_to_wheat_farm(self, tile):
        self.navigate_to(tile)

    def destination_reached(self):
        if self.current_tile.get_building().get_build_type() == BuildingTypes.WHEAT_FARM:
            print("Hit The Farm")
            print(self.associated_building)
            self.navigate_to(self.associated_building)
            
        
        elif self.current_tile.get_building().get_build_type() == BuildingTypes.GRANARY:
            print("Back to my granary")
        