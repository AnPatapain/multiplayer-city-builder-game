from buildable.structure import Structure
from class_types.buildind_types import BuildingTypes
from game.game_controller import GameController
from walkers.final.granary_worker import Granary_worker

class Granary(Structure):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, BuildingTypes.GRANARY, max_employee=6, fire_risk=0, destruction_risk=0)
        self.food_stocked = 0
        self.max_food_stocked = 100
        self.game_controller = GameController.get_instance()
        self.wheat_farm_tiles = []


    def new_walker(self):
        if self.associated_walker:
            print("A walker is already assigned to this building!")
            return

        tile = self.find_adjacent_road()
        if tile:
            self.associated_walker = Granary_worker(self)
            self.associated_walker.spawn(tile)

    def get_all_farm_tiles(self): 
        from buildable.final.structures.WheatFarm import WheatFarm

        grid = self.game_controller.get_map()
        self.wheat_farm_tiles = []

        for row in grid:
            for tile in row:
                building = tile.get_building()
                if isinstance(building, WheatFarm) and tile.get_show_tile():
                    self.wheat_farm_tiles.append(building.get_current_tile())

        return self.wheat_farm_tiles.copy()
        

    def update_day(self):
        super().update_day()
        if not self.associated_walker:
            self.new_walker()

    def receive_wheat_from_worker(self, wheat): self.food_stocked += wheat