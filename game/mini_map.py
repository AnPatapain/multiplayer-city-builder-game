import pygame as pg

from class_types.buildind_types import BuildingTypes
from class_types.tile_types import TileTypes
from events.event_manager import EventManager
from game.game_controller import GameController
from game.map_controller import MapController
from game.setting import GRID_SIZE
from map_element.tile import Tile


class MiniMap:
    def __init__(self) -> None:
        self.mini_screen_width = 48
        self.mini_screen_height = 27

        self.mm_width = 145
        self.mm_height = 111

        # Create a surface that matches the size of the map, we will transform it later to have the wanted size
        self.background = pg.Surface((GRID_SIZE, GRID_SIZE)).convert()

        self.camera_zone_rect = None

        self.pos_x = 1920 - self.mm_width - 8
        self.pos_y = 81  # 46 = topbar height

        self.mini_relative_x = None
        self.mini_relative_y = None

        EventManager.register_mouse_listener(self.mini_map_mouse_listener)

    def render_map(self):
        grid = GameController.get_instance().get_map()
        buff = pg.surfarray.pixels2d(self.background)
        for row in grid:
            for tile in row:
                color = self.get_color(tile)
                buff[tile.y][tile.x] = self.background.map_rgb(color)

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
        else:
            self.mini_relative_x = None
            self.mini_relative_y = None

    def update(self):
        if self.mini_relative_x and self.mini_relative_y:
            corresponding_x = - (self.mini_relative_x - self.mini_screen_width / 2) / 0.035
            corresponding_y = - (self.mini_relative_y - self.mini_screen_height / 2) / 0.0665
            MapController.set_map_pos(corresponding_x, corresponding_y)
        # Only render every 10 ticks (5 times per second
        if GameController.get_instance().current_tick % 25 == 0:
            self.render_map()

    def draw(self, screen: pg.Surface):
        # We need coordination of 4 points to draw rhombus
        map_pos = MapController.get_map_pos()
        self.camera_zone_rect = pg.Rect(- map_pos[0] * 0.035,
                                        - map_pos[1] * 0.0665,
                                        self.mini_screen_width, self.mini_screen_height)

        temp_bg = self.background.copy()
        # The rotation will take the color on the topleft corner to add padding
        temp_bg.set_at((0, 0), (0, 0, 0))
        temp_bg = pg.transform.rotate(temp_bg, -45)
        temp_bg = pg.transform.scale(temp_bg, (self.mm_width, self.mm_height))

        pg.draw.rect(temp_bg, (255, 255, 0), self.camera_zone_rect, 1)
        screen.blit(temp_bg, (self.pos_x, self.pos_y))

    def get_color(self, tile: Tile) -> tuple[int, int, int]:
        b = tile.get_building()
        if b:
            if b.build_type in [BuildingTypes.ROCK, BuildingTypes.BIG_ROCK]:
                return (120, 120, 120)  # Gray
            if b.build_type == BuildingTypes.TREE:
                return (0, 100, 0)  # Dark green
            return (255, 140, 0)  # Orange

        if tile.get_road():
            return (153, 76, 0)  # Brown

        match tile.type:
            case TileTypes.WATER:
                return (0, 92, 184)  # Blue
            case TileTypes.WHEAT:
                return (220, 220, 0)  # Bold yellow
            case TileTypes.GRASS:
                return (76, 153, 0)  # Green
