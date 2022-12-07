import pygame as pg
from game.setting import DEFAULT_SURFACE_WIDTH, DEFAULT_SURFACE_HEIGHT
from events.event_manager import EventManager
from .mapcontroller import MapController

class MiniMap:
    scale_down_ratio = 0.1

    def __init__(self, width, height, event_manager: EventManager) -> None:
        self.event_manager = event_manager

        self.screen_width = width
        self.screen_height = height

        self.mini_screen_width = MiniMap.scale_down_ratio * width
        self.mini_screen_height = MiniMap.scale_down_ratio * height

        self.mini_default_surface_width = MiniMap.scale_down_ratio * DEFAULT_SURFACE_WIDTH
        self.mini_default_surface_height = MiniMap.scale_down_ratio * DEFAULT_SURFACE_HEIGHT

        self.mini_default_surface = pg.Surface((self.mini_default_surface_width, self.mini_default_surface_height))

        self.mini_screen_rect = None

        self.mini_map_pos_x = self.screen_width - self.mini_default_surface_width
        self.mini_map_pos_y = self.screen_height * 0.04

        self.mini_relative_x = None
        self.mini_relative_y = None

        self.event_manager.register_mouse_listener(self.mini_map_mouse_listener)
        print(self.event_manager.mouse_listeners)


    def mini_map_mouse_listener(self):
        mouse_pos = pg.mouse.get_pos()
        mouse_action = pg.mouse.get_pressed()

        (x, y) = mouse_pos
        if (self.mini_map_pos_x <= x <= self.screen_width) and (self.mini_map_pos_y < y <= self.mini_map_pos_y + self.mini_default_surface_height):
            if mouse_action[0]:
                self.mini_relative_x = x - self.mini_map_pos_x
                self.mini_relative_y = y - self.mini_map_pos_y
            else:
                self.mini_relative_x = None
                self.mini_relative_y = None


    def update(self, map_controller: MapController):
        if self.mini_relative_x is not None and self.mini_relative_y is not None:
            corresponding_x = - (self.mini_relative_x - self.mini_screen_width/2) / self.scale_down_ratio
            corresponding_y = - (self.mini_relative_y - self.mini_screen_height/2) / self.scale_down_ratio
            map_controller.set_map_pos(corresponding_x, corresponding_y)
        

    def draw(self, screen, map_pos):
        self.mini_default_surface.fill((0, 0, 0))
        # We need coordination of 4 points to draw rhombus
        pg.draw.polygon(self.mini_default_surface, (0, 255, 0),
                        [(self.mini_default_surface_width / 2, 0),
                         (self.mini_default_surface_width, self.mini_default_surface_height / 2),
                         (self.mini_default_surface_width / 2, self.mini_default_surface_height),
                         (0, self.mini_default_surface_height / 2)], 1)

        self.mini_screen_rect = pg.Rect(- map_pos[0] * MiniMap.scale_down_ratio,
                                        - map_pos[1] * MiniMap.scale_down_ratio,
                                        self.mini_screen_width, self.mini_screen_height)

        pg.draw.rect(self.mini_default_surface, (255, 255, 0), self.mini_screen_rect, 1)
        screen.blit(self.mini_default_surface, (self.mini_map_pos_x, self.mini_map_pos_y))