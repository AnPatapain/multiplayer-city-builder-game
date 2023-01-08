from buildable.structure import Structure
from class_types.buildind_types import BuildingTypes
from game.game_controller import GameController
from game.textures import Textures
from game.setting import *
import pygame as pg

class WheatFarm(Structure):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, BuildingTypes.WHEAT_FARM, build_size=(3, 3), max_employee=10,fire_risk=1,destruction_risk=1)
        self.game_controller = GameController.get_instance()
        self.wheat_soil_pos: list[(int, int)] | None = self.get_wheat_soil_pos()
        self.wheat_quantity = 0
        self.max_wheat = 100

        self.farm_img = Textures.get_texture(BuildingTypes.WHEAT_FARM)
        self.wheat_sol_img = Textures.get_texture(BuildingTypes.WHEAT_SOIL_LEVEL_5)

        #++++++++++++++++++++ TESTING PURPOSE +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        self.relax_days = 10 # just for testing for seeing the evolution of soil
        

    def get_texture(self):
        farm_img_height = self.farm_img.get_height()
        farm_img_width = self.farm_img.get_width()

        rendered = pg.Surface( (116*3, farm_img_height + 60) ).convert_alpha()

        rendered.blit(self.farm_img, ( ( rendered.get_width() - farm_img_width )/2, 0))
        
        #soil 1
        rendered.blit(self.wheat_sol_img, (0, farm_img_height - 60 - (self.wheat_sol_img.get_height() - TILE_SIZE) ) )
        #soil2
        rendered.blit(self.wheat_sol_img, (58, farm_img_height - 60 - (self.wheat_sol_img.get_height() - TILE_SIZE) + 30 ))
        
        #soil 4
        rendered.blit(self.wheat_sol_img, (58*4, farm_img_height - 60 - (self.wheat_sol_img.get_height() - TILE_SIZE)))
        
        #soil 2
        rendered.blit(self.wheat_sol_img, (58*3, farm_img_height - 60 - (self.wheat_sol_img.get_height() - TILE_SIZE) + 30))

        #soil 3
        rendered.blit(self.wheat_sol_img, (58*2, farm_img_height - 60 - (self.wheat_sol_img.get_height() - TILE_SIZE) + 30*2 ))
        
        return rendered.convert_alpha()


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
        pass
        # self.relax_days -= 1
        # if self.is_upgradable():
        #     self.produce_wheat()

        #     #Update the image of the wheat soil around the farm 
        #     for wheat_soil in self.get_wheat_soils():
        #         print(wheat_soil)
        #         wheat_soil.upgrade()
        #         self.relax_days = 10 # Reset relax days for workers : ) whenever they produce one level
    
    def is_upgradable(self):
        '''
        TODO: check whether the workers in Wheat Farm has enough food to work (I think so). 
            For now return True if we don't produce enough wheat 
        '''
        return (not self.atteindre_max_quantity() and self.relax_days == 0)
        
    
