import pygame as pg

from class_types.tile_types import TileTypes
from class_types.panel_types import BuildingButtonTypes, SwitchViewButtonTypes
from components.button import Button
from components.image_button import ButtonImage
from game.textures import Textures
from game.utils import draw_text
import os

class Panel:
    
    def __init__(self, width, height, event_manager):
        self.width, self.height = width, height

        self.event_manager = event_manager

        self.ressource_panel_color = (204, 174, 132)
        self.building_panel_color = (230, 162, 64)

        # Ressource panel in the top of screen
        self.ressource_panel = pg.Surface((self.width, self.height * 0.043))
        self.ressource_panel_rect = self.ressource_panel.get_rect(topleft=(0, 0))
        self.ressource_panel.fill(self.ressource_panel_color)

        # Building panel in the right screen
        self.building_panel = pg.Surface((self.width * 0.2, self.height * 0.96))
        self.building_panel_rect = self.building_panel.get_rect(topleft=(self.width * 0.8, self.height * 0.04))
        self.building_panel.fill(self.building_panel_color)

        # Available building in building panel
        self.buildings = self.load_images()

        self.build__tree = ButtonImage((self.building_panel_rect.left + 20, 800), (120, 80), Textures.get_texture(TileTypes.TREE))
        self.build__tree.on_click(lambda: self.set_selected_tile(TileTypes.TREE))

        self.build__rock = ButtonImage((self.building_panel_rect.left + 20 + 120 + 20, 800), (120, 80), Textures.get_texture(TileTypes.ROCK))
        self.build__rock.on_click(lambda: self.set_selected_tile(TileTypes.ROCK))

        self.event_manager.register_component(self.build__tree)
        self.event_manager.register_component(self.build__rock)

        # Selected building (defaultly, nothing is selected)
        self.selected_tile = None
        self.panel_rects = [self.ressource_panel_rect, self.building_panel_rect]


    def draw(self, screen):        
        screen.blit(self.ressource_panel, (0, 0))
        screen.blit(self.building_panel, (self.width * 0.8, self.height * 0.04))

        screen.blit(Textures.get_texture(SwitchViewButtonTypes.BARRE), (0, 0))
        screen.blit(Textures.get_texture(SwitchViewButtonTypes.BARRE), (500, 0))

        screen.blit(Textures.get_texture(SwitchViewButtonTypes.DYNAMIC_DISPLAY), (1000, 0))
        screen.blit(Textures.get_texture(SwitchViewButtonTypes.DYNAMIC_DISPLAY), (1000 - 304, 0))

        screen.blit(Textures.get_texture(SwitchViewButtonTypes.SCULPTURE), (self.width - 162, self.height -120))
        screen.blit(Textures.get_texture(SwitchViewButtonTypes.MINI_SCULPTURE), (self.width - 155, self.height * 0.043 + 216))
        screen.blit(Textures.get_texture(SwitchViewButtonTypes.JULIUS), (self.width - 155, 200))
        screen.blit(Textures.get_texture(SwitchViewButtonTypes.EUROPEAN), (self.width - 78, 200))

        screen.blit(Textures.get_texture(SwitchViewButtonTypes.BUTTON1), (self.width - 155, 230))
        screen.blit(Textures.get_texture(SwitchViewButtonTypes.BUTTON2), (self.width - 116, 230))
        screen.blit(Textures.get_texture(SwitchViewButtonTypes.BUTTON3), (self.width - 78, 230))
        screen.blit(Textures.get_texture(SwitchViewButtonTypes.BUTTON4), (self.width - 39, 230))

        screen.blit(Textures.get_texture(SwitchViewButtonTypes.BUTTON5), (self.width - 150, 277 + 46))
        screen.blit(Textures.get_texture(SwitchViewButtonTypes.BUTTON6), (self.width - 100, 277 + 46))
        screen.blit(Textures.get_texture(SwitchViewButtonTypes.BUTTON7), (self.width - 49, 277 + 46))
        screen.blit(Textures.get_texture(SwitchViewButtonTypes.BUTTON8), (self.width - 150, 312 + 46))
        screen.blit(Textures.get_texture(SwitchViewButtonTypes.BUTTON9), (self.width - 100, 312 + 46))
        screen.blit(Textures.get_texture(SwitchViewButtonTypes.BUTTON10), (self.width - 49, 312 + 46))
        screen.blit(Textures.get_texture(SwitchViewButtonTypes.BUTTON11), (self.width - 150, 349 + 46))
        screen.blit(Textures.get_texture(SwitchViewButtonTypes.BUTTON12), (self.width - 100, 349 + 46))
        screen.blit(Textures.get_texture(SwitchViewButtonTypes.BUTTON13), (self.width - 49, 349 + 46))
        screen.blit(Textures.get_texture(SwitchViewButtonTypes.BUTTON14), (self.width - 150, 385 + 46))
        screen.blit(Textures.get_texture(SwitchViewButtonTypes.BUTTON15), (self.width - 100, 385 + 46))
        screen.blit(Textures.get_texture(SwitchViewButtonTypes.BUTTON16), (self.width - 49, 385 + 46))
        screen.blit(Textures.get_texture(SwitchViewButtonTypes.BUTTON17), (self.width - 150, 420 + 46))
        screen.blit(Textures.get_texture(SwitchViewButtonTypes.BUTTON18), (self.width - 100, 420 + 46))
        screen.blit(Textures.get_texture(SwitchViewButtonTypes.BUTTON19), (self.width - 49, 420 + 46))


        screen.blit(Textures.get_texture(SwitchViewButtonTypes.TOP_PANNEL), (self.width - 162, self.height * 0.043))
        screen.blit(Textures.get_texture(SwitchViewButtonTypes.BOTTOM_PANNEL), (self.width - 162, 496))

        resource_panel_text  = ['File', 'Options', 'Help', 'Advisor', 'Dn: 0', 'Population: 0']
        
        resource_panel_text_pos = [20, 10]
        i=0
        for text in resource_panel_text:

            temp_pos = resource_panel_text_pos.copy()

            draw_text(text, screen, temp_pos, size=38)

            if(i>=3):
                resource_panel_text_pos[0] += 280
            else:
                resource_panel_text_pos[0] += 150
            i+=1


        self.build__tree.display(screen)
        self.build__rock.display(screen)

    
    def update(self):
        pass
        # self.event_manager.handle_events()


    def load_images(self):    
        path = 'assets/C3_sprites/C3'

        return {

            'tree': self.scale_image_2x( pg.image.load(os.path.join(path, 'Land1a_00041.png')) ).convert_alpha(),
            'rock': self.scale_image_2x( pg.image.load(os.path.join(path, 'Land1a_00290.png')) ).convert_alpha()

        }

    
    def scale_image(self, image, width=None, height=None): # Procedure function which scales up or down the image specified 
        # Default case do nothing
        if (width == None) and (height == None):
            pass

        elif height == None: # scale only width
            scale = width / image.get_width()
            height = scale * image.get_height()
            image = pg.transform.scale(image, ( int(width), int(height) ))

        elif width == None: # scale only width
            scale = height / image.get_height()
            width = scale * image.get_width()
            image = pg.transform.scale(image, (int(width), int(height)))

        else:
            image = pg.transform.scale(image, (int(width), int(height)))

        return image


    def scale_image_2x(self, image):
        return pg.transform.scale2x(image)

    def has_selected_tile(self): return self.selected_tile is not None

    def get_selected_tile(self): return self.selected_tile

    def set_selected_tile(self, value): self.selected_tile = value

    def get_panel_rects(self): return self.panel_rects