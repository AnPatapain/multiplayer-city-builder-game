from buildable.structure import Structure
from class_types.buildind_types import BuildingTypes
from game.textures import Textures
from game.setting import *
import pygame as pg
from game.game_controller import GameController

class WheatFarm(Structure):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, BuildingTypes.WHEAT_FARM, max_employee=10, fire_risk=0, destruction_risk=0)
        self.wheat_quantity = 0
        self.max_wheat = 100

        self.farm_img = Textures.get_texture(BuildingTypes.WHEAT_FARM)
        self.wheat_sol_img = Textures.get_texture(BuildingTypes.WHEAT_SOIL_LEVEL_1)
        self.game_controller = GameController.get_instance()

        #++++++++++++++++++++ TESTING PURPOSE +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        self.relax_days = 10 # just for testing for seeing the evolution of soil
        

    def get_texture(self):
        farm_img_height = self.farm_img.get_height()
        farm_img_width = self.farm_img.get_width()

        rendered = pg.Surface( (116*3, farm_img_height + 60), pg.SRCALPHA, 32)
        rendered = rendered.convert_alpha()

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
        
        return rendered

    def get_delete_texture(self):
        texture = self.get_texture().copy()
        Textures.fill(texture)
        return texture

    def get_wheat_quantities(self): return self.wheat_quantity

    def set_wheat_soil_img(self, img): self.wheat_sol_img = img

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
            match self.get_wheat_quantities():
                case 20: self.set_wheat_soil_img(Textures.get_texture(BuildingTypes.WHEAT_SOIL_LEVEL_1))
                case 40: self.set_wheat_soil_img(Textures.get_texture(BuildingTypes.WHEAT_SOIL_LEVEL_2))
                case 60: self.set_wheat_soil_img(Textures.get_texture(BuildingTypes.WHEAT_SOIL_LEVEL_3))
                case 80: self.set_wheat_soil_img(Textures.get_texture(BuildingTypes.WHEAT_SOIL_LEVEL_4))
                case 100: self.set_wheat_soil_img(Textures.get_texture(BuildingTypes.WHEAT_SOIL_LEVEL_5))

            if self.atteindre_max_quantity():
                self.wheat_quantity = 0
            self.relax_days = 10

    def move_wheat_to_granary(self):
        '''
        TODO: Order the associated worker move the wheat to granary 
        '''
        from buildable.final.structures.granary import Granary
        pass

    def is_upgradable(self):
        '''
        TODO: check whether the workers in Wheat Farm has enough food to work (I think so). 
            For now return True if we don't produce enough wheat 
        '''
        return (not self.atteindre_max_quantity() and self.relax_days == 0)
        
    
