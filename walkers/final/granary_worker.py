from buildable.buildable import Buildable
from class_types.buildind_types import BuildingTypes
from buildable.house import House
from buildable.structure import Structure
from class_types.walker_types import WalkerTypes
from walkers.walker import Walker
from game.textures import Textures
from buildable.final.structures.WheatFarm import WheatFarm
from enum import Enum

class Actions(Enum):
    IDLE = 0
    GO_TO_FARM = 1
    GO_TO_GRANARY = 2


class Granary_worker(Walker):
    def __init__(self, associated_building: Buildable):
        super().__init__(WalkerTypes.GRANARY_WORKER, associated_building, roads_only=True)
        self.current_action = Actions.IDLE
        self.actual_wheat = 0

    def go_to_wheat_farm(self, tile):
        self.navigate_to(tile)

    def get_action(self): return self.current_action

    def set_action(self, action): self.current_action = action

    def destination_reached(self):
        from buildable.final.structures.granary import Granary
        print(self.current_tile.get_building(), self.current_tile.get_show_tile())

        if self.current_tile.get_building().get_build_type() == BuildingTypes.WHEAT_FARM:
            farm: WheatFarm = self.current_tile.get_building()
            self.receive_wheat_from_farm(farm)
            self.navigate_to(self.associated_building.get_current_tile())
            

        elif self.current_tile.get_building().get_build_type() == BuildingTypes.GRANARY:
            print("Back to my granary")
            myGranary: Granary = self.current_tile.get_building()
            self.move_wheat_to_granary(myGranary)

    def receive_wheat_from_farm(self, farm: WheatFarm):   
        self.actual_wheat += farm.given_wheat_to_granary_worker()

    def move_wheat_to_granary(self, granary):
        granary.receive_wheat_from_worker(self.actual_wheat)
        self.actual_wheat = 0