import pygame as pg
import game.setting as Setting
from events.event_manager import EventManager
from .mapcontroller import MapController

class MiniMap:
    scale_down_ratio = 0.1

    def __init__(self, screen, width, height, event_manager: EventManager) -> None:
        self.event_manager = event_manager

        self.screen = screen
        self.screen_width = width
        self.screen_height = height

        self.mini_screen_width = MiniMap.scale_down_ratio * width
        self.mini_screen_height = MiniMap.scale_down_ratio * height

        self.mini_default_surface_width = MiniMap.scale_down_ratio * Setting.DEFAULT_SURFACE_WIDTH
        self.mini_default_surface_height = MiniMap.scale_down_ratio * Setting.DEFAULT_SURFACE_HEIGHT

        self.mini_map_pos_x = self.screen_width - self.mini_default_surface_width
        self.mini_map_pos_y = self.screen_height * 0.04

        self.mini_default_surface = self.mini_default_surface()

        self.mini_screen_rect = None

        self.mini_relative_pos = None 
        self.pos_on_big_map = None

        self.event_manager.register_mouse_listener(self.mini_map_mouse_listener)


    def mini_default_surface(self):
        mini_df_surface = pg.Surface((self.mini_default_surface_width, self.mini_default_surface_height))
        mini_df_surface.fill((0, 0, 0))
        return mini_df_surface


    def draw(self, map_pos):

        self.screen.blit(self.mini_default_surface, (self.mini_map_pos_x, self.mini_map_pos_y))

        # We need coordination of 4 points to draw rhombus
        pg.draw.polygon(self.screen, (0, 255, 0),
                        [(self.mini_map_pos_x + self.mini_default_surface_width / 2, self.mini_map_pos_y),
                         (self.mini_map_pos_x + self.mini_default_surface_width,
                          self.mini_map_pos_y + self.mini_default_surface_height / 2),
                         (self.mini_map_pos_x + self.mini_default_surface_width / 2,
                          self.mini_map_pos_y + self.mini_default_surface_height),
                         (self.mini_map_pos_x, self.mini_map_pos_y + self.mini_default_surface_height / 2)], 1)

        if self.is_in_mini_map(self.mini_map_pos_x - map_pos[0] * MiniMap.scale_down_ratio,
                               self.mini_map_pos_y - map_pos[1] * MiniMap.scale_down_ratio):
            self.mini_screen_rect = pg.Rect(self.mini_map_pos_x - map_pos[0] * MiniMap.scale_down_ratio,
                                            self.mini_map_pos_y - map_pos[1] * MiniMap.scale_down_ratio,
                                            self.mini_screen_width, self.mini_screen_height)

        if self.mini_screen_rect is not None:
            pg.draw.rect(self.screen, (255, 255, 0), self.mini_screen_rect, 1)

    def mini_map_mouse_listener(self):
        mouse_position = pg.mouse.get_pos()
        mouse_action = pg.mouse.get_pressed()
        (x, y) = mouse_position

        if self.is_in_mini_map(x, y) and mouse_action[0]:
            print("coucou")
            #Transform mouse postion to relative position to mini_default_surface
            self.mini_relative_pos = [x - self.mini_map_pos_x, y - self.mini_map_pos_y]
            #Deduce the position on the big map by inversing the function which is used for converting pos on big map to pos on mini_map
            self.pos_on_big_map = [-self.mini_relative_pos[0]/self.scale_down_ratio, 
                                   -self.mini_relative_pos[1]/self.scale_down_ratio]

    def update(self, map_controller_instance):
        if self.pos_on_big_map != None:
            map_controller_instance.set_map_pos(self.pos_on_big_map[0], self.pos_on_big_map[1])

    def is_in_mini_map(self, x, y):
        in_x = (
                    self.mini_map_pos_x + self.mini_default_surface_width - self.mini_screen_width >= x >= self.mini_map_pos_x)
        in_y = (
                    self.mini_map_pos_y <= y <= self.mini_map_pos_y + self.mini_default_surface_height - self.mini_screen_height)

        if in_x and in_y:
            return True
        return False
