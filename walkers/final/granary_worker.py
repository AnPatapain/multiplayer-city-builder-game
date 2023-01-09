from buildable.buildable import Buildable
from class_types.buildind_types import BuildingTypes
from buildable.house import House
from buildable.structure import Structure
from class_types.walker_types import WalkerTypes
from walkers.walker import Walker
from game.textures import Textures
from enum import Enum

class Actions(Enum):
    IDLE = 0
    GO_TO_FARM = 1
    GO_TO_GRANARY = 2


class Granary_worker(Walker):
    def __init__(self, associated_building: Buildable):
        super().__init__(WalkerTypes.GRANARY_WORKER, associated_building, roads_only=True)
        self.current_action = Actions.IDLE

    def go_to_wheat_farm(self, tile):
        self.navigate_to(tile)

    def get_action(self): return self.current_action

    def set_action(self, action): self.current_action = action

    def destination_reached(self):
        if self.current_tile.get_building().get_build_type() == BuildingTypes.WHEAT_FARM:
            self.navigate_to(self.associated_building.get_current_tile())
            
        elif self.current_tile.get_building().get_build_type() == BuildingTypes.GRANARY:
            print("Back to my granary")
        