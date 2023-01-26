from buildable.structure import Structure
from class_types.buildind_types import BuildingTypes
from game.textures import Textures
from game.setting import *
import pygame as pg
from game.game_controller import GameController
from walkers.final.farm_worker import Farm_worker

class WheatFarm(Structure):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, BuildingTypes.WHEAT_FARM, max_employee=10, fire_risk=0, destruction_risk=0)
        self.wheat_quantity = 0
        self.max_wheat = 80
        #++++++++++++++++++++ TESTING PURPOSE +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        self.relax_days = 10 # just for testing for seeing the evolution of soil
        

    def get_texture(self):
        if self.atteindre_max_quantity():
            return Textures.get_texture(BuildingTypes.WHEAT_FARM, 4)
        return Textures.get_texture(BuildingTypes.WHEAT_FARM, self.wheat_quantity//20)

    def get_delete_texture(self):
        if self.atteindre_max_quantity():
            return Textures.get_delete_texture(BuildingTypes.WHEAT_FARM, 4)
        return Textures.get_delete_texture(BuildingTypes.WHEAT_FARM, self.wheat_quantity//20)

    def get_wheat_quantities(self): return self.wheat_quantity

    def produce_wheat(self):
        self.wheat_quantity += 20

    def atteindre_max_quantity(self):
        return self.wheat_quantity == self.max_wheat

    def is_upgradable(self):
        '''
        TODO: check whether the workers in Wheat Farm has enough food to work (I think so). 
            For now return True if we don't produce enough wheat 
        '''
        return (not self.atteindre_max_quantity() and self.relax_days == 0)


    def give_wheat_to_worker(self):
        if self.atteindre_max_quantity():
            given_wheat_quantity = self.wheat_quantity
            self.wheat_quantity = 0
            return given_wheat_quantity
        else:
            return 0

            
    def update_day(self):
        super().update_day()
        #Spawn the farm worker
        if not self.associated_walker:
            self.new_walker()
        if self.relax_days > 0:
            self.relax_days -= 1
        # print("ready to produce: ", self.is_upgradable())

        if self.is_upgradable():
            self.produce_wheat()
            self.relax_days = 10


    def new_walker(self):
        if self.associated_walker:
            print("A walker is already assigned to this building!")
            return

        tile = self.find_adjacent_road()
        if tile:
            self.associated_walker = Farm_worker(self)
            self.associated_walker.spawn(tile)
