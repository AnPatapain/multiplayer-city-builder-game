from buildable.structure import Structure
from class_types.buildind_types import BuildingTypes
from game.textures import Textures
from game.setting import *
import pygame as pg
from game.game_controller import GameController
from walkers.final.granary_worker import Granary_worker

class Granary(Structure):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, BuildingTypes.GRANARY, build_size=(3, 3), max_employee=6, fire_risk=0, destruction_risk=0)
        self.food_stocked = 0
        self.max_food_stocked = 100
        self.game_controller = GameController.get_instance()

    def new_walker(self):
        if self.associated_walker:
            print("A walker is already assigned to this building!")
            return

        tile = self.find_adjacent_road()
        if tile:
            self.associated_walker = Granary_worker(self)
            self.associated_walker.spawn(tile)

    def order_workers_to_get_wheat(self):
        from buildable.final.structures.WheatFarm import WheatFarm
        from walkers.final.granary_worker import Actions

        grid = self.game_controller.get_map()
        wheat_farms = []
        
        for row in grid:
            for tile in row:
                building = tile.get_building()
                if isinstance(building, WheatFarm) and tile.get_show_tile():
                    wheat_farms.append(building.get_current_tile())

        
        for wheat_farm in wheat_farms:
            worker: Granary_worker = self.associated_walker
            if len(worker.path_to_destination) == 0:
                worker.go_to_wheat_farm(wheat_farm)
            worker.set_action(Actions.GO_TO_FARM)
        

    def update_day(self):
        super().update_day()
        if not self.associated_walker:
            self.new_walker()
        else:
            self.order_workers_to_get_wheat()
        print(self.food_stocked)

    def receive_wheat_from_worker(self, wheat): self.food_stocked += wheat