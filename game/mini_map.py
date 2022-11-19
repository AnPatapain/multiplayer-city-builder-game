import pygame as pg
import game.setting as Setting

class MiniMap:

    scale_down_ratio = 0.1

    def __init__(self, screen, width, height) -> None:
        self.screen = screen
        self.screen_width = width
        self.screen_height = height
        
        self.mini_screen_width = MiniMap.scale_down_ratio * width
        self.mini_screen_height = MiniMap.scale_down_ratio * height

        self.mini_default_surface_width = MiniMap.scale_down_ratio * Setting.DEFAULT_SURFACE_WIDTH
        self.mini_default_surface_height = MiniMap.scale_down_ratio * Setting.DEFAULT_SURFACE_HEIGHT

        self.mini_default_surface = pg.Surface((self.mini_default_surface_width, self.mini_default_surface_height))
        self.mini_default_surface.fill((0, 0, 0))

        self.mini_screen_rect = None

        self.mini_map_pos_x = self.screen_width - self.mini_default_surface_width
        self.mini_map_pos_y = self.screen_height * 0.04

    def draw(self, map_pos):
        
        self.screen.blit(self.mini_default_surface, (self.mini_map_pos_x, self.mini_map_pos_y))

        # We need coordination of 4 points to draw rhombus
        pg.draw.polygon(self.screen, (0, 255, 0), [(self.mini_map_pos_x + self.mini_default_surface_width/2, self.mini_map_pos_y),
                                                   (self.mini_map_pos_x + self.mini_default_surface_width, self.mini_map_pos_y + self.mini_default_surface_height/2),
                                                   (self.mini_map_pos_x + self.mini_default_surface_width/2, self.mini_map_pos_y + self.mini_default_surface_height),
                                                   (self.mini_map_pos_x, self.mini_map_pos_y + self.mini_default_surface_height/2)], 1)
        


        if self.is_in_mini_map(self.mini_map_pos_x - map_pos[0]*MiniMap.scale_down_ratio, self.mini_map_pos_y - map_pos[1]*MiniMap.scale_down_ratio):
            self.mini_screen_rect = pg.Rect(self.mini_map_pos_x - map_pos[0]*MiniMap.scale_down_ratio, self.mini_map_pos_y - map_pos[1]*MiniMap.scale_down_ratio, 
                                   self.mini_screen_width, self.mini_screen_height)

        if self.mini_screen_rect is not None:
            pg.draw.rect(self.screen, (255, 255, 0), self.mini_screen_rect, 1)

    def update():
        pass


    def is_in_mini_map(self, x, y):
        if (self.mini_map_pos_x + self.mini_default_surface_width > x > self.mini_map_pos_x) and ( self.mini_map_pos_y <= y <= self.mini_map_pos_y + self.mini_default_surface_height ):
            return True
        return False