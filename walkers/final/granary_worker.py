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
    IN_THE_WAY_TO_FARM = 1
    IN_THE_WAY_TO_GRANARY = 2


class Granary_worker(Walker):
    def __init__(self, associated_building: Buildable):
        super().__init__(WalkerTypes.GRANARY_WORKER, associated_building, roads_only=True)
        self.current_action = Actions.IDLE
        self.wheat_in_hand = 0
        self.current_farm_tiles_list = [] # list of farm tile
        self.is_finish_in_one_farm = False

    def go_to_farm_tile(self, tile):
        self.navigate_to(tile)

    def receive_wheat_from_farm(self, farm: WheatFarm):   
        self.actual_wheat += farm.given_wheat_to_granary_worker()

    def move_wheat_to_granary(self, granary):
        granary.receive_wheat_from_worker(self.actual_wheat)
        self.actual_wheat = 0


    def update(self):
        from buildable.final.structures.granary import Granary
        super().update()
        myGranary: Granary = self.associated_building

        if len(self.current_farm_tiles_list) == 0:
            self.current_farm_tiles_list = myGranary.get_all_farm_tiles()

        # Traverse all the farm in queue
        while len(self.current_farm_tiles_list) != 0:
            if self.current_action == Actions.IDLE:
                self.go_to_farm_tile(self.current_farm_tiles_list[0])
                self.current_action = Actions.IN_THE_WAY_TO_FARM # update the current action

    def destination_reached(self):
        from buildable.final.structures.granary import Granary
        # print(self.current_tile.get_building(), self.current_tile.get_show_tile())

        if self.current_tile.get_building().get_build_type() == BuildingTypes.WHEAT_FARM:
            print("Hit the farm")
            farm: WheatFarm = self.current_tile.get_building()
            # self.receive_wheat_from_farm(farm)
            self.navigate_to(self.associated_building.get_current_tile())
            self.current_action = Actions.IN_THE_WAY_TO_GRANARY
            self.current_farm_tiles_list.pop(0)
            

        elif self.current_tile.get_building().get_build_type() == BuildingTypes.GRANARY:
            print("Back to my granary")
            self.current_action = Actions.IDLE
            # myGranary: Granary = self.current_tile.get_building()
            # self.move_wheat_to_granary(myGranary)
