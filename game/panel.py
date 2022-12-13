import pygame as pg

from class_types.tile_types import TileTypes
from class_types.road_types import RoadTypes
from class_types.buildind_types import BuildingTypes
from components.button import Button
from game.textures import Textures
from game.utils import draw_text
from events.event_manager import EventManager

class Panel:
    
    def __init__(self, width, height):
        self.width, self.height = width, height


        self.ressource_panel_color = (204, 174, 132)
        self.building_panel_color = (230, 162, 64)

        # Ressource panel in the top of screen
        self.ressource_panel = pg.Surface((self.width, self.height * 0.04))
        self.ressource_panel_rect = self.ressource_panel.get_rect(topleft=(0, 0))
        self.ressource_panel.fill(self.ressource_panel_color)

        # Building panel in the right screen
        self.building_panel = pg.Surface((self.width * 0.2, self.height * 0.96))
        self.building_panel_rect = self.building_panel.get_rect(topleft=(self.width * 0.8, self.height * 0.04))
        self.building_panel.fill(self.building_panel_color)

        self.build__tree = Button((self.building_panel_rect.left + 20, 800), (120, 80), image=Textures.get_texture(TileTypes.TREE))
        self.build__tree.on_click(lambda: self.set_selected_tile(TileTypes.TREE))

        self.build__rock = Button((self.building_panel_rect.left + 20 + 120 + 20, 800), (120, 80), image=Textures.get_texture(TileTypes.ROCK))
        self.build__rock.on_click(lambda: self.set_selected_tile(TileTypes.ROCK))

        self.build__road = Button((self.building_panel_rect.left + 20, 800 + 80 + 20), (120, 80), image=Textures.get_texture(RoadTypes.TL_TO_BR))
        self.build__road.on_click(lambda: self.set_selected_tile(RoadTypes.TL_TO_BR))

        self.build__small_tent = Button((self.building_panel_rect.left + 20, 700), (120, 80), image=Textures.get_texture(BuildingTypes.SMALL_TENT))
        self.build__small_tent.on_click(lambda: self.set_selected_tile(BuildingTypes.SMALL_TENT))

        self.build__large_tent = Button((self.building_panel_rect.left + 20 + 120, 700), (120, 80), image=Textures.get_texture(BuildingTypes.LARGE_TENT))
        self.build__large_tent.on_click(lambda: self.set_selected_tile(BuildingTypes.LARGE_TENT))

        self.build__small_shack = Button((self.building_panel_rect.left + 20, 600), (120, 80), image=Textures.get_texture(BuildingTypes.LARGE_SHACK))
        self.build__small_shack.on_click(lambda: self.set_selected_tile(BuildingTypes.LARGE_SHACK))

        self.build__large_shack = Button((self.building_panel_rect.left + 20 + 120, 600), (120, 80), image=Textures.get_texture(BuildingTypes.LARGE_SHACK))
        self.build__large_shack.on_click(lambda: self.set_selected_tile(BuildingTypes.LARGE_SHACK))


        EventManager.register_component(self.build__tree)
        EventManager.register_component(self.build__rock)
        EventManager.register_component(self.build__road)
        EventManager.register_component(self.build__small_tent)
        EventManager.register_component(self.build__large_tent)
        EventManager.register_component(self.build__small_shack)
        EventManager.register_component(self.build__large_shack)

        # Selected building (defaultly, nothing is selected)
        self.selected_tile = None
        self.panel_rects = [self.ressource_panel_rect, self.building_panel_rect]


    def draw(self, screen):        
        screen.blit(self.ressource_panel, (0, 0))

        screen.blit(self.building_panel, (self.width * 0.8, self.height * 0.04))

        resource_panel_text = ['File', 'Options', 'Help', 'Advisor', 'Dn: 0', 'Population: 0']
        
        resource_panel_text_pos = [20, 20]

        for text in resource_panel_text:
            
            temp_pos = resource_panel_text_pos.copy()

            draw_text(text, screen, temp_pos, size=42)
            
            resource_panel_text_pos[0] += 200

        self.build__tree.display(screen)
        self.build__rock.display(screen)
        self.build__road.display(screen)
        self.build__small_tent.display(screen)
        self.build__large_tent.display(screen)
        self.build__small_shack.display(screen)
        self.build__large_shack.display(screen)

    
    def update(self):
        pass


    def scale_image(self, image, width=None, height=None):  # Procedure function which scales up or down the image specified
        # Default case do nothing
        if (width is None) and (height is None):
            pass

        elif height is None:  # scale only width
            scale = width / image.get_width()
            height = scale * image.get_height()
            image = pg.transform.scale(image, ( int(width), int(height) ))

        elif width is None:  # scale only width
            scale = height / image.get_height()
            width = scale * image.get_width()
            image = pg.transform.scale(image, (int(width), int(height)))

        else:
            image = pg.transform.scale(image, (int(width), int(height)))

        return image

    def has_selected_tile(self): return self.selected_tile is not None

    def get_selected_tile(self): return self.selected_tile

    def set_selected_tile(self, value): self.selected_tile = value

    def get_panel_rects(self): return self.panel_rects
