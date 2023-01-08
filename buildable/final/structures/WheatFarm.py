from buildable.structure import Structure
from class_types.buildind_types import BuildingTypes
from game.game_controller import GameController

class WheatFarm(Structure):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, BuildingTypes.WHEAT_FARM, build_size=(3, 3), max_employee=10,fire_risk=1,destruction_risk=1)
        self.game_controller = GameController.get_instance()
        self.wheat_soil_pos: list[(int, int)] | None = self.get_wheat_soil_pos()
        self.wheat_quantity = 0
        self.max_wheat = 100

        #++++++++++++++++++++ TESTING PURPOSE +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        self.relax_days = 10 # just for testing for seeing the evolution of soil
        

    def get_wheat_soil_pos(self):
        row, col = self.x, self.y
        print(self.game_controller)
        map = self.game_controller.get_map()
        if map[row][col].get_show_tile():
            return [
                (row + 1, col),
                (row + 1, col + 1),
                (row + 1, col + 2),
                (row, col + 2),
                (row - 1, col + 2)
            ]
        return None
    
    def get_wheat_soils(self):
        map = self.game_controller.get_map()
        return [map[row][col].get_building() for (row, col) in self.get_wheat_soil_pos()]

    def produce_wheat(self):
        if not self.atteindre_max_quantity():
            # We have 5 level of wheat soil around the farm so i think each level correspond to 20 quantity of wheat (I can't find it in docs)
            self.wheat_quantity += 20

    def atteindre_max_quantity(self):
        return self.wheat_quantity == self.max_wheat

    def update_day(self):
        self.relax_days -= 1
        if self.is_upgradable():
            self.produce_wheat()

            #Update the image of the wheat soil around the farm 
            for wheat_soil in self.get_wheat_soils():
                print(wheat_soil)
                wheat_soil.upgrade()
                self.relax_days = 10 # Reset relax days for workers : ) whenever they produce one level
    
    def is_upgradable(self):
        '''
        TODO: check whether the workers in Wheat Farm has enough food to work (I think so). 
            For now return True if we don't produce enough wheat 
        '''
        return (not self.atteindre_max_quantity() and self.relax_days == 0)
        
    
