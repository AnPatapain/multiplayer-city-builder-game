import pygame as pg

from buildable.final.rock import Rock
from buildable.final.tree import SmallTree
from events.event_manager import EventManager
from .gameController import GameController
from .mapcontroller import MapController
from .setting import *

from map_element.tile import Tile
from class_types.tile_types import TileTypes


class MiniMap:
    def __init__(self) -> None:
        self.mini_screen_width = 48
        self.mini_screen_height = 27

        self.mm_width = 145
        self.mm_height = 111

        # Create a surface that matches the size of the map, we will transform it later to have the wanted size
        self.background = pg.Surface((50, 50)).convert()

        self.camera_zone_rect = None

        self.pos_x = 1920 - self.mm_width - 8
        self.pos_y = 81  # 46 = topbar height

        self.mini_relative_x = None
        self.mini_relative_y = None

        EventManager.register_mouse_listener(self.mini_map_mouse_listener)


    def background_generator(self, logic_grid):
        for row in range(NUMS_GRID_Y):
            for col in range(NUMS_GRID_X):
                tile: Tile = logic_grid[row][col]
                color = self.get_color(tile)
                
                self.background.set_at((col, row), color)

    def background_update(self, logic_grid):
        for row in range(NUMS_GRID_Y):
            for col in range(NUMS_GRID_X):
                tile: Tile = logic_grid[row][col]
                color = self.get_color(tile)

                if tile.type != TileTypes.GRASS or tile.get_building():
                    self.background.set_at((col, row), color)

                # In case we delete something in the world
                elif tile.type == TileTypes.GRASS:
                    self.background.set_at((col, row), (76, 153, 0))

    def mini_map_mouse_listener(self):
        mouse_pos = pg.mouse.get_pos()
        mouse_action = pg.mouse.get_pressed()

        (x, y) = mouse_pos
        if (self.pos_x <= x <= 1920 - 8) and (self.pos_y < y <= self.pos_y + self.mm_height):
            if mouse_action[0]:
                self.mini_relative_x = x - self.pos_x
                self.mini_relative_y = y - self.pos_y
            else:
                self.mini_relative_x = None
                self.mini_relative_y = None


    def update(self):
        if self.mini_relative_x is not None and self.mini_relative_y is not None:
            corresponding_x = - (self.mini_relative_x - self.mini_screen_width/2) / 0.025
            corresponding_y = - (self.mini_relative_y - self.mini_screen_height/2) / 0.0465
            MapController.set_map_pos(corresponding_x, corresponding_y)
        self.background_update(GameController.get_instance().get_map())
        

    def draw(self, screen):
        # We need coordination of 4 points to draw rhombus

        map_pos = MapController.get_map_pos()
        self.camera_zone_rect = pg.Rect(- map_pos[0] * 0.025,
                                        - map_pos[1] * 0.0465,
                                        self.mini_screen_width, self.mini_screen_height)

        temp_bg = self.background.copy()
        # The rotation will take the color on the topleft corner to add padding
        temp_bg.set_at((0, 0), (0, 0, 0))
        temp_bg = pg.transform.rotate(temp_bg, -45)
        temp_bg = pg.transform.scale(temp_bg, (self.mm_width, self.mm_height))

        pg.draw.rect(temp_bg, (255, 255, 0), self.camera_zone_rect, 1)
        screen.blit(temp_bg, (self.pos_x, self.pos_y))


    def get_color(self, tile: Tile):
        if tile.get_building():
            if isinstance(tile.get_building(), Rock):
                return (96, 96, 96)
            if isinstance(tile.get_building(), SmallTree):
                return (204, 255, 204)
            return (255, 255, 0) # yellow

        if tile.get_road():
            return (153, 76, 0) # brown

        match tile.type:
            case TileTypes.WATER: return (102, 178, 255) # blue
            case TileTypes.WHEAT: return (204, 204, 0) # Bold yellow
            case TileTypes.GRASS: return (76, 153, 0)
