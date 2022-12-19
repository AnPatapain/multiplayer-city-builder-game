import pygame as pg
from events.event_manager import EventManager
from .mapcontroller import MapController
from .setting import *

from map_element.tile import Tile
from class_types.tile_types import TileTypes
from class_types.road_types import RoadTypes
from .utils import scale_image
from .textures import Textures

class MiniMap:
    def __init__(self, logic_grid) -> None:
        self.mini_screen_width = 48
        self.mini_screen_height = 27

        self.mm_width = 145
        self.mm_height = 111

        self.background = pg.Surface((self.mm_width, self.mm_height))
        self.background.fill((0, 0, 0))
        pg.draw.polygon(self.background, (0, 255, 0),
                        [(self.mm_width / 2, 0),
                         (self.mm_width, self.mm_height / 2),
                         (self.mm_width / 2, self.mm_height),
                         (0, self.mm_height / 2)], 1)

        self.camera_zone_rect = None

        # self.pos_x = width - self.mm_width - 8
        self.pos_x = 1920 - self.mm_width - 8
        self.pos_y = 81  # 46 = topbar height

        self.mini_relative_x = None
        self.mini_relative_y = None

        self.background_generator(logic_grid)

        EventManager.register_mouse_listener(self.mini_map_mouse_listener)

    def mini_default_surface_generator(self, logic_grid):
        for row in range(NUMS_GRID_Y):
            for col in range(NUMS_GRID_X):
                tile: Tile = logic_grid[row][col]
                (x, y) = tile.get_render_coord()
                # cell is placed at 1/2 default_surface.get_width() and be offseted by the position of the default_surface
                (x_offset, y_offset) = (x + DEFAULT_SURFACE_WIDTH / 2, y)
                (mini_x_offset, mini_y_offset) = (x_offset*MiniMap.scale_down_ratio, y_offset*MiniMap.scale_down_ratio)
                texture_image = Textures.get_texture(TileTypes.GRASS)
                mini_texture_image = scale_image(texture_image, texture_image.get_width()*MiniMap.scale_down_ratio, texture_image.get_height()*MiniMap.scale_down_ratio)
                
                self.mini_default_surface.blit(mini_texture_image,
                                              (mini_x_offset, mini_y_offset - texture_image.get_height() + TILE_SIZE))

    def mini_map_mouse_listener(self):
        mouse_pos = pg.mouse.get_pos()
        mouse_action = pg.mouse.get_pressed()

        (x, y) = mouse_pos
        if (self.pos_x <= x <= 1920) and (self.pos_y < y <= self.pos_y + self.mm_height):
            if mouse_action[0]:
                self.mini_relative_x = x - self.pos_x
                self.mini_relative_y = y - self.pos_y
            else:
                self.mini_relative_x = None
                self.mini_relative_y = None


    def update(self):
        if self.mini_relative_x is not None and self.mini_relative_y is not None:
            corresponding_x = - (self.mini_relative_x - self.mini_screen_width/2) / 0.025
            corresponding_y = - (self.mini_relative_y - self.mini_screen_height/2) / 0.037
            MapController.set_map_pos(corresponding_x, corresponding_y)
        

    def draw(self, screen, map_pos):
        # We need coordination of 4 points to draw rhombus
        self.camera_zone_rect = pg.Rect(- map_pos[0] * 0.024,
                                        - map_pos[1] * 0.037,
                                        self.mini_screen_width, self.mini_screen_height)

        temp_bg = self.background.copy()
        pg.draw.rect(temp_bg, (255, 255, 0), self.camera_zone_rect, 1)
        screen.blit(temp_bg, (self.pos_x, self.pos_y))


    def get_color(self, tile: Tile):
        color = (0, 255, 0)
        if tile.get_building() is not None: 
            return (255, 255, 0) #yellow

        if tile.get_road() is not None:
            # brown
            return (153, 76, 0)

        match tile.type:
            case TileTypes.WATER: return (102, 178, 255) #blue
            
            case TileTypes.WHEAT: return (204, 204, 0) #Bold yellow

            case TileTypes.ROCK: return (96, 96, 96) #Gray

            case TileTypes.GRASS: return (76, 153, 0) 

            case TileTypes.TREE: return (204, 255, 204)