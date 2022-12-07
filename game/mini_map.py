import pygame as pg
from game.setting import DEFAULT_SURFACE_WIDTH, DEFAULT_SURFACE_HEIGHT

class MiniMap:

    scale_down_ratio = 0.0249

    def __init__(self, width, height) -> None:
        self.screen_width = width
        self.screen_height = height

        self.mini_screen_width = MiniMap.scale_down_ratio * width
        self.mini_screen_height = MiniMap.scale_down_ratio * height

        self.mini_default_surface_width = MiniMap.scale_down_ratio * DEFAULT_SURFACE_WIDTH
        self.mini_default_surface_height = MiniMap.scale_down_ratio * DEFAULT_SURFACE_HEIGHT

        self.mini_default_surface = pg.Surface((self.mini_default_surface_width, self.mini_default_surface_height))

        self.mini_screen_rect = None

        # self.mini_map_pos_x = self.screen_width - self.mini_default_surface_width
        # self.mini_map_pos_y = self.screen_height * 0.04
        self.mini_map_pos_x = self.screen_width - self.mini_default_surface_width - 8
        self.mini_map_pos_y = 98

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
