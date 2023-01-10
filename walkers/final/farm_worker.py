from buildable.buildable import Buildable
from class_types.buildind_types import BuildingTypes
from buildable.house import House
from class_types.walker_types import WalkerTypes
from walkers.walker import Walker
from enum import Enum

class Actions(Enum):
    IDLE = 0
    IN_THE_WAY_TO_FARM = 1
    IN_THE_WAY_TO_GRANARY = 2


class Farm_worker(Walker):
    def __init__(self, associated_building: Buildable):
        super().__init__(WalkerTypes.FARM_WORKER, associated_building, roads_only=True)
        self.current_action = Actions.IDLE
        self.wheat_in_hand = 0
        self.current_granary_list = [] # list of farm tile


    def move_wheat_in_hand_to_granary(self, granary):
        from buildable.final.structures.granary import Granary
        granary: Granary = granary
        granary.receive_wheat_from_farm_worker(self.wheat_in_hand)


    def get_food_from_associated_farm(self):
        from buildable.final.structures.WheatFarm import WheatFarm
        myFarm: WheatFarm = self.associated_building
        self.wheat_in_hand = myFarm.give_wheat_to_worker()  


    def update(self):
        from buildable.final.structures.WheatFarm import WheatFarm
        super().update()
        myFarm: WheatFarm = self.associated_building

        if len(self.current_granary_list) == 0:
            self.current_granary_list = myFarm.get_all_granary_tiles()

        # print(self.current_granary_list, self.current_action)
        # print(self.current_action)
        # if self.current_action == Actions.IDLE: print("je fait rien")

        # Traverse the farm at the beginning of the queue
        if len(self.current_granary_list) != 0:
            if self.current_action == Actions.IDLE:
                self.navigate_to(self.current_granary_list[0])
                self.current_action = Actions.IN_THE_WAY_TO_GRANARY # update the current action


    def destination_reached(self):
        # print(self.current_tile.get_building(), self.current_tile.get_show_tile())
        building = self.current_tile.get_building()

        if building.get_build_type() == BuildingTypes.GRANARY:
            # print("Hit the granary")
            self.move_wheat_in_hand_to_granary(building)
            self.navigate_to(self.associated_building.get_current_tile()) #back to the farm
            self.current_action = Actions.IN_THE_WAY_TO_FARM
            self.current_granary_list.pop(0)
            

        elif building.get_build_type() == BuildingTypes.WHEAT_FARM:
            # print("Back to my farm")
            self.get_food_from_associated_farm()
            self.current_action = Actions.IDLE
