import pygame as pg

from class_types.buildind_types import BuildingTypes
from class_types.panel_types import SwitchViewButtonTypes
from class_types.road_types import RoadTypes
from components.button import Button
from events.event_manager import EventManager
from game.game_controller import GameController
from game.mini_map import MiniMap
from game.textures import Textures
from game.utils import draw_text
from map_element.tile import Tile
from game.overlay import Overlay

TOPBAR_HEIGHT = 46
PANEL_WIDTH = 162
PANEL_HEIGHT = 1080 - TOPBAR_HEIGHT

class Panel:
    def __init__(self, width, height):
        self.width, self.height = width, height

        # Mini_Map
        self.mini_map = MiniMap()

        self.ressource_panel_color = (204, 174, 132)
        self.building_panel_color = (230, 162, 64)

        # Ressource panel in the top of screen
        self.ressource_panel = pg.Surface((self.width, TOPBAR_HEIGHT)).convert()
        self.ressource_panel_rect = self.ressource_panel.get_rect(topleft=(0, 0))
        self.ressource_panel.fill(self.ressource_panel_color)
        self.ressource_panel.blit(Textures.get_texture(SwitchViewButtonTypes.BARRE), (0, 0))
        self.ressource_panel.blit(Textures.get_texture(SwitchViewButtonTypes.BARRE), (500, 0))
        self.ressource_panel.blit(Textures.get_texture(SwitchViewButtonTypes.DYNAMIC_DISPLAY), (1000, 0))
        self.ressource_panel.blit(Textures.get_texture(SwitchViewButtonTypes.DYNAMIC_DISPLAY), (1000 - 304, 0))

        # Building panel in the right screen
        self.building_panel = pg.Surface((PANEL_WIDTH, self.height)).convert()
        self.building_panel_rect = self.building_panel.get_rect(topleft=(self.width - PANEL_WIDTH, TOPBAR_HEIGHT))
        self.building_panel.fill(self.building_panel_color)
        self.building_panel.blit(Textures.get_texture(SwitchViewButtonTypes.TOP_PANNEL), (0, 0))
        self.building_panel.blit(Textures.get_texture(SwitchViewButtonTypes.BOTTOM_PANNEL), (0, 496 - TOPBAR_HEIGHT))
        self.building_panel.blit(Textures.get_texture(SwitchViewButtonTypes.SCULPTURE), (0, PANEL_HEIGHT - 120))
        self.building_panel.blit(Textures.get_texture(SwitchViewButtonTypes.MINI_SCULPTURE), (7, 216))
        self.building_panel.blit(Textures.get_texture(SwitchViewButtonTypes.JULIUS), (7, 200 - TOPBAR_HEIGHT))
        self.building_panel.blit(Textures.get_texture(SwitchViewButtonTypes.EUROPEAN), (84, 200 - TOPBAR_HEIGHT))

        # Overlay button
        self.change_overlay = Button((self.width - 158, 49), (117,25), text_fn=Overlay.get_instance().get_name,
                                     center_text=True,text_size=30)
        self.change_overlay.on_click(lambda: Overlay.get_instance().set_overlay_types())

        button_size = (39, 26)
        self.build__road = Button((self.width - 49, 277 + TOPBAR_HEIGHT), button_size,
                                  image=Textures.get_texture(SwitchViewButtonTypes.BUTTON7),
                                  image_hover=Textures.get_texture(SwitchViewButtonTypes.BUTTON7_HOVER),
                                  image_selected=Textures.get_texture(SwitchViewButtonTypes.BUTTON7_SELECTED),
                                  disable_unselect=True, selectable=True)
        self.build__road.on_click(lambda: self.set_selected_tile(RoadTypes.TL_TO_BR))

        self.destroy_tile = Button((self.width - 99, 277 + TOPBAR_HEIGHT), button_size,
                                   image=Textures.get_texture(SwitchViewButtonTypes.BUTTON6),
                                   image_hover=Textures.get_texture(SwitchViewButtonTypes.BUTTON6_HOVER),
                                   image_selected=Textures.get_texture(SwitchViewButtonTypes.BUTTON6_SELECTED),
                                   disable_unselect=True, selectable=True)
        self.destroy_tile.on_click(lambda: self.set_selected_tile(BuildingTypes.PELLE))  # image qui est sur le curseur

        self.build__house = Button((self.width - 149, 277 + TOPBAR_HEIGHT), button_size,
                                   image=Textures.get_texture(SwitchViewButtonTypes.BUTTON5),
                                   image_hover=Textures.get_texture(SwitchViewButtonTypes.BUTTON5_HOVER),
                                   image_selected=Textures.get_texture(SwitchViewButtonTypes.BUTTON5_SELECTED),
                                   disable_unselect=True, selectable=True)
        self.build__house.on_click(lambda: self.set_selected_tile(BuildingTypes.VACANT_HOUSE))

        self.build__prefecture = Button((self.width - 99, 385 + TOPBAR_HEIGHT), button_size,
                                        image=Textures.get_texture(SwitchViewButtonTypes.BUTTON15),
                                        image_hover=Textures.get_texture(SwitchViewButtonTypes.BUTTON15_HOVER),
                                        image_selected=Textures.get_texture(SwitchViewButtonTypes.BUTTON15_SELECTED),
                                        disable_unselect=True, selectable=True)
        self.build__prefecture.on_click(lambda: self.set_selected_tile(BuildingTypes.PREFECTURE))

        self.build__well = Button((self.width - 149, 312 + TOPBAR_HEIGHT), button_size,
                                  image=Textures.get_texture(SwitchViewButtonTypes.BUTTON8),
                                  image_hover=Textures.get_texture(SwitchViewButtonTypes.BUTTON8_HOVER),
                                  image_selected=Textures.get_texture(SwitchViewButtonTypes.BUTTON8_SELECTED),
                                  disable_unselect=True, selectable=True)
        self.build__well.on_click(lambda: self.set_selected_tile(BuildingTypes.WELL))

        self.build__engineer_post = Button((self.width - 149, 385 + TOPBAR_HEIGHT), button_size,
                                   image=Textures.get_texture(SwitchViewButtonTypes.BUTTON14),
                                   image_hover=Textures.get_texture(SwitchViewButtonTypes.BUTTON14_HOVER),
                                   image_selected=Textures.get_texture(SwitchViewButtonTypes.BUTTON14_SELECTED),
                                   disable_unselect=True, selectable=True)
        self.build__engineer_post.on_click(lambda: self.set_selected_tile(BuildingTypes.ENGINEERS_POST))

        self.increase_speed = Button((self.width - 149, 490 + TOPBAR_HEIGHT), button_size,
                                     image=Textures.get_texture(SwitchViewButtonTypes.INCREASE_SPEED),
                                     image_hover=Textures.get_texture(SwitchViewButtonTypes.INCREASE_SPEED_HOVER),
                                     image_selected=Textures.get_texture(SwitchViewButtonTypes.INCREASE_SPEED_SELECTED))
        self.increase_speed.on_click(GameController.get_instance().increase_current_speed)

        self.decrease_speed = Button((self.width - 100, 490 + TOPBAR_HEIGHT), button_size,
                                     image=Textures.get_texture(SwitchViewButtonTypes.DECREASE_SPEED),
                                     image_hover=Textures.get_texture(SwitchViewButtonTypes.DECREASE_SPEED_HOVER),
                                     image_selected=Textures.get_texture(SwitchViewButtonTypes.DECREASE_SPEED_SELECTED))
        self.decrease_speed.on_click(GameController.get_instance().decrease_current_speed)

        EventManager.register_component(self.destroy_tile)
        EventManager.register_component(self.build__house)
        EventManager.register_component(self.build__prefecture)
        EventManager.register_component(self.build__road)
        EventManager.register_component(self.build__well)
        EventManager.register_component(self.build__engineer_post)
        EventManager.register_component(self.change_overlay)
        EventManager.register_component(self.increase_speed)
        EventManager.register_component(self.decrease_speed)


        # Selected building (defaultly, nothing is selected)
        self.selected_tile = None
        self.panel_rects = [self.ressource_panel_rect, self.building_panel_rect]

    def draw(self, screen):
        screen.blit(self.ressource_panel, (0, 0))
        screen.blit(self.building_panel, (self.width - 162, TOPBAR_HEIGHT))

        screen.blit(Textures.get_texture(SwitchViewButtonTypes.BARRE), (0, 0))
        screen.blit(Textures.get_texture(SwitchViewButtonTypes.BARRE), (500, 0))
        screen.blit(Textures.get_texture(SwitchViewButtonTypes.DYNAMIC_DISPLAY), (1000, 0))
        screen.blit(Textures.get_texture(SwitchViewButtonTypes.DYNAMIC_DISPLAY), (1000 - 304, 0))
        screen.blit(Textures.get_texture(SwitchViewButtonTypes.DYNAMIC_DISPLAY), (1000 + 304, 0))


        screen.blit(Textures.get_texture(SwitchViewButtonTypes.SCULPTURE), (self.width - 162, self.height - 120))
        screen.blit(Textures.get_texture(SwitchViewButtonTypes.MINI_SCULPTURE), (self.width - 155, self.height * 0.043 + 216))
        screen.blit(Textures.get_texture(SwitchViewButtonTypes.JULIUS), (self.width - 155, 200))
        screen.blit(Textures.get_texture(SwitchViewButtonTypes.EUROPEAN), (self.width - 78, 200))
        # Can't draw on the building_panel because we need absolute position to move the camera with the mouse listener
        self.mini_map.draw(screen)

        screen.blit(Textures.get_texture(SwitchViewButtonTypes.BUTTON1), (self.width - 155, 230))
        screen.blit(Textures.get_texture(SwitchViewButtonTypes.BUTTON2), (self.width - 116, 230))
        screen.blit(Textures.get_texture(SwitchViewButtonTypes.BUTTON3), (self.width - 78, 230))
        screen.blit(Textures.get_texture(SwitchViewButtonTypes.BUTTON4), (self.width - 39, 230))
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


        resource_panel_text = ['File', 'Options', 'Help', 'Advisor']
        resource_panel_text_pos = [20, 10]
        i = 0
        for text in resource_panel_text:
            draw_text(text, screen, resource_panel_text_pos, color=(50, 30, 0), size=38)
            if i >= 3:
                resource_panel_text_pos[0] += 280
            else:
                resource_panel_text_pos[0] += 150
            i += 1

        self.build__road.display(screen)
        self.destroy_tile.display(screen)
        self.build__house.display(screen)
        self.build__prefecture.display(screen)
        self.build__well.display(screen)
        self.build__engineer_post.display(screen)
        self.change_overlay.display(screen)
        self.increase_speed.display(screen)
        self.decrease_speed.display(screen)


    def update(self):
        self.mini_map.update()

    def has_selected_tile(self):
        return self.selected_tile is not None

    def get_selected_tile(self) -> Tile:
        return self.selected_tile

    def set_selected_tile(self, value):
        self.selected_tile = value
        if value is None:
            self.build__prefecture.set_selected(False)
            self.build__house.set_selected(False)
            self.build__well.set_selected(False)
            self.build__road.set_selected(False)
            self.destroy_tile.set_selected(False)

    def get_panel_rects(self):
        return self.panel_rects

    def get_mini_map(self): return self.mini_map
