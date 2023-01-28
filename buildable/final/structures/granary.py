from buildable.structure import Structure
from class_types.buildind_types import BuildingTypes
from game.game_controller import GameController
from walkers.final.granary_worker import Granary_worker
from game.textures import Textures

class Granary(Structure):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, BuildingTypes.GRANARY, max_employee=6, fire_risk=0, destruction_risk=0)
        self.wheat_stocked = 0
        # self.max_food_stocked = 100
        self.game_controller = GameController.get_instance()
        self.wheat_farm_tiles = []

    def get_texture(self):
        if self.wheat_stocked >= 320:
            return Textures.get_texture(BuildingTypes.GRANARY, 4)
        return Textures.get_texture(BuildingTypes.GRANARY, self.wheat_stocked//80)


    def receive_wheat_from_farm_worker(self, wheat_quantity): 
        self.wheat_stocked += wheat_quantity
    
    def get_wheat_stocked(self):
        return self.wheat_stocked

    def update_day(self):
        super().update_day()
        