import pygame as pg

from class_types.road_types import RoadTypes
from class_types.panel_types import SwitchViewButtonTypes
from components.button import Button
from game.textures import Textures
from game.utils import draw_text
from map_element.tile import Tile
from events.event_manager import EventManager


class Panel:
    
    def __init__(self, width, height):
        self.width, self.height = width, height

        self.ressource_panel_color = (204, 174, 132)
        self.building_panel_color = (230, 162, 64)

        # Ressource panel in the top of screen
        self.ressource_panel = pg.Surface((self.width, self.height * 0.043))
        self.ressource_panel_rect = self.ressource_panel.get_rect(topleft=(0, 0))
        self.ressource_panel.fill(self.ressource_panel_color)

        # Building panel in the right screen
        self.building_panel = pg.Surface((self.width * 0, self.height * 0.96))
        self.building_panel_rect = self.building_panel.get_rect(topleft=(self.width * 0.8, self.height * 0.04))
        self.building_panel.fill(self.building_panel_color)

        button_size = (39, 26)
        self.build__road = Button((self.width - 49, 277 + 46), button_size,
                                  image=Textures.get_texture(SwitchViewButtonTypes.BUTTON7),
                                  image_hover=Textures.get_texture(SwitchViewButtonTypes.BUTTON7_HOVER),
                                  image_selected=Textures.get_texture(SwitchViewButtonTypes.BUTTON7_SELECTED))
        self.build__road.on_click(lambda: self.set_selected_tile(RoadTypes.TL_TO_BR))

        self.destroy_tile = Button((self.width - 99, 277 + 46), button_size,
                                   image=Textures.get_texture(SwitchViewButtonTypes.BUTTON6),
                                   image_hover=Textures.get_texture(SwitchViewButtonTypes.BUTTON6_HOVER),
                                   image_selected=Textures.get_texture(SwitchViewButtonTypes.BUTTON6_SELECTED))
        self.destroy_tile.on_click(lambda: self.set_selected_tile(BuildingTypes.PELLE))  # image qui est sur le curseur

        self.build__house = Button((self.width - 149, 277 + 46), button_size,
                                   image=Textures.get_texture(SwitchViewButtonTypes.BUTTON5),
                                   image_hover=Textures.get_texture(SwitchViewButtonTypes.BUTTON5_HOVER),
                                   image_selected=Textures.get_texture(SwitchViewButtonTypes.BUTTON5_SELECTED))
        self.build__house.on_click(lambda: self.set_selected_tile(BuildingTypes.SMALL_TENT))

        self.build__prefecture = Button((self.width - 99, 385 + 46), button_size,
                                        image=Textures.get_texture(SwitchViewButtonTypes.BUTTON15),
                                        image_hover=Textures.get_texture(SwitchViewButtonTypes.BUTTON15_HOVER),
                                        image_selected=Textures.get_texture(SwitchViewButtonTypes.BUTTON15_SELECTED))
        self.build__prefecture.on_click(lambda: self.set_selected_tile(BuildingTypes.PREFECTURE))

        EventManager.register_component(self.destroy_tile)
        EventManager.register_component(self.build__house)
        EventManager.register_component(self.build__prefecture)
        EventManager.register_component(self.build__road)

        # Selected building (defaultly, nothing is selected)
        self.selected_tile = None
        self.panel_rects = [self.ressource_panel_rect, self.building_panel_rect]

    def draw(self, screen):
        screen.blit(self.ressource_panel, (0, 0))
        screen.blit(self.building_panel, (self.width * 0.8, self.height * 0.04))

        resource_panel_text = ['File', 'Options', 'Help', 'Advisor', 'Dn: 0', 'Population: 0']
        screen.blit(Textures.get_texture(SwitchViewButtonTypes.BARRE), (0, 0))
        screen.blit(Textures.get_texture(SwitchViewButtonTypes.BARRE), (500, 0))
        screen.blit(Textures.get_texture(SwitchViewButtonTypes.DYNAMIC_DISPLAY), (1000, 0))
        screen.blit(Textures.get_texture(SwitchViewButtonTypes.DYNAMIC_DISPLAY), (1000 - 304, 0))

        screen.blit(Textures.get_texture(SwitchViewButtonTypes.SCULPTURE), (self.width - 162, self.height - 120))
        screen.blit(Textures.get_texture(SwitchViewButtonTypes.MINI_SCULPTURE), (self.width - 155, self.height * 0.043 + 216))
        screen.blit(Textures.get_texture(SwitchViewButtonTypes.JULIUS), (self.width - 155, 200))
        screen.blit(Textures.get_texture(SwitchViewButtonTypes.EUROPEAN), (self.width - 78, 200))

        screen.blit(Textures.get_texture(SwitchViewButtonTypes.BUTTON1), (self.width - 155, 230))
        screen.blit(Textures.get_texture(SwitchViewButtonTypes.BUTTON2), (self.width - 116, 230))
        screen.blit(Textures.get_texture(SwitchViewButtonTypes.BUTTON3), (self.width - 78, 230))
        screen.blit(Textures.get_texture(SwitchViewButtonTypes.BUTTON4), (self.width - 39, 230))
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

        resource_panel_text = ['File', 'Options', 'Help', 'Advisor', 'Dn: 0', 'Population: 0']

        resource_panel_text_pos = [20, 10]
        i = 0
        for text in resource_panel_text:

            temp_pos = resource_panel_text_pos.copy()

            draw_text(text, screen, temp_pos, size=38)

            if i >= 3:
                resource_panel_text_pos[0] += 280
            else:
                resource_panel_text_pos[0] += 150
            i += 1

        self.build__road.display(screen)
        self.destroy_tile.display(screen)
        self.build__house.display(screen)
        self.build__prefecture.display(screen)

    def update(self):
        pass

    def scale_image(self, image, width=None,
                    height=None):  # Procedure function which scales up or down the image specified
        # Default case do nothing
        if (width is None) and (height is None):
            pass

        elif height is None:  # scale only width
            scale = width / image.get_width()
            height = scale * image.get_height()
            image = pg.transform.scale(image, (int(width), int(height)))

        elif width is None:  # scale only width
            scale = height / image.get_height()
            width = scale * image.get_width()
            image = pg.transform.scale(image, (int(width), int(height)))

        else:
            image = pg.transform.scale(image, (int(width), int(height)))

        return image

    def has_selected_tile(self):
        return self.selected_tile is not None

    def get_selected_tile(self) -> Tile:
        return self.selected_tile

    def set_selected_tile(self, value):
        self.selected_tile = value

    def get_panel_rects(self):
        return self.panel_rects
