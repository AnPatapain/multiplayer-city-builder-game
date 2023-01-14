import random
from typing import Optional, TYPE_CHECKING
import pygame as pg

from buildable.road import Road
from class_types.buildind_types import BuildingTypes
from class_types.tile_types import TileTypes
from game.game_controller import GameController
from game.textures import Textures
from game.setting import TILE_SIZE, GRID_SIZE

if TYPE_CHECKING:
    from buildable.buildable import Buildable
    from walkers.walker import Walker


class Tile:
    def __init__(self, col: int, row: int, tile_type: TileTypes = TileTypes.GRASS):
        self.type = tile_type
        self.building: Optional[Buildable] = None
        self.show_tile = True
        self.road: Road | None = None
        self.x = row
        self.y = col

        self.random_texture_number = 0
        self.water_access = False

        self.walkers: list['Walker'] = []

        cartesian_coord = [
            (col * TILE_SIZE, row * TILE_SIZE),
            (col * TILE_SIZE + TILE_SIZE, row * TILE_SIZE),
            (col * TILE_SIZE + TILE_SIZE, row * TILE_SIZE + TILE_SIZE),
            (col * TILE_SIZE, row * TILE_SIZE + TILE_SIZE)
        ]

        def convert_cartesian_to_isometric(x, y):
            return x - y, (x + y) / 2

        self.isometric_coord = [convert_cartesian_to_isometric(x, y) for x, y in cartesian_coord]
        self.render_coord = (
            min([x for x, y in self.isometric_coord]),
            min([y for x, y in self.isometric_coord])
        )

    def set_random_texture_number(self, num: int):
        self.random_texture_number = num

    def get_random_texture_number(self) -> int:
        return self.random_texture_number

    def set_water_texture(self, type):
        self.water_texture = type

    def get_water_texture(self):
        return self.water_texture

    def get_render_coord(self):
        return self.render_coord

    def get_isometric_coord(self):
        return self.isometric_coord

    def get_type(self):
        return self.type

    def set_type(self, new_type):
        self.type = new_type

    def get_water_access(self):
        return self.water_access

    def set_water_access(self, water_access: bool):
        self.water_access = water_access

    def get_building(self) -> 'Buildable':
        return self.building

    def set_building(self, new_building, show_building: bool = True):
        self.building = new_building
        self.show_tile = show_building

    def get_road(self) -> Road | None:
        return self.road

    def set_road(self, new_road):
        self.road = new_road

    def set_show_tile(self, show_tile: bool):
        self.show_tile = show_tile

    def get_show_tile(self):
        return self.show_tile

    def get_texture(self):
        if not self.show_tile:
            return Textures.get_texture(TileTypes.GRASS)
        if self.building:
            return self.building.get_texture()
        if self.road:
            return Textures.get_texture(self.road.get_road_type())
        return Textures.get_texture(self.type, texture_number=self.random_texture_number)

    def get_delete_texture(self):
        if not self.show_tile:
            return Textures.get_texture(TileTypes.GRASS)
        if self.road:
            return Textures.get_delete_texture(self.road.get_road_type())
        if self.building:
            return self.building.get_delete_texture()
        return Textures.get_delete_texture(self.type)

    def is_buildable(self, build_size: tuple[int, int] = (1, 1)):
        grid = GameController.get_instance().get_map()
        for x in range(build_size[0]):
            for y in range(build_size[1]):
                if self.x - x < 0 or self.y + y > GRID_SIZE-1:
                    return False

                tile = grid[self.x - x][self.y + y]
                if tile.get_building() or tile.get_road() or tile.type not in (TileTypes.WHEAT, TileTypes.GRASS):
                    return False

        return True

    def is_destroyable(self):
        real_tile = self
        # Ensure we check to the left of the building
        if self.get_building():
            real_tile = self.get_building().get_current_tile()
        return (real_tile.show_tile and real_tile.building and real_tile.building.is_destroyable()) or real_tile.road

    def destroy(self):
        if self.building:
            self.building.destroy()
            self.building = None
        self.road = None
        self.show_tile = True
        for walker in self.walkers:
            walker.associated_building.associated_walker.delete()

    def add_walker(self, walker: 'Walker'):
        self.walkers.append(walker)

    def remove_walker(self, walker: 'Walker'):
        self.walkers.remove(walker)

    def get_adjacente_tiles(self, radius: int = 0):
        adjacentes_tiles = []

        grid = GameController.get_instance().get_map()

        if radius == 0:
            coords = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        else:
            coords = [(x, y) for y in range(-radius, radius+1) for x in range(-radius, radius+1)]

        for coord in coords:
            try:
                if self.x + coord[0] > GRID_SIZE-1 or self.y + coord[1] > GRID_SIZE-1 or self.x + coord[0] < 0 or self.y + coord[1] < 0:
                    continue
                adjacentes_tiles.append(grid[self.x + coord[0]][self.y + coord[1]])
            except IndexError:
                continue

        return adjacentes_tiles

    def find_path_to(self, dest: list['Tile'], roads_only: bool = False, buildable_or_road: bool = False) -> list['Tile']:
        def _estimate_distance(src: 'Tile') -> int:
            dest_x = abs(abs(src.x) - abs(self.x))
            dest_y = abs(abs(src.y) - abs(self.y))
            return dest_x + dest_y

        open_set: list['Tile'] = [self]
        came_from: dict['Tile', 'Tile'] = {}
        g_score: dict['Tile', int] = {self: 0}
        f_score: dict['Tile', int] = {self: _estimate_distance(self)}

        if isinstance(dest, Tile):
            dest = [dest]

        while len(open_set) > 0:
            open_set.sort(key=lambda tile: (f_score[tile]))
            current = open_set.pop(0)

            if current in dest:
                path_to_destination = []
                path_to_destination.insert(0, current)
                while current in came_from:
                    current = came_from[current]
                    path_to_destination.insert(0, current)

                return path_to_destination

            for neighbor in current.get_adjacente_tiles():
                if roads_only and not neighbor.get_road() and neighbor not in dest:
                    continue
                if buildable_or_road and (not neighbor.is_buildable() and not neighbor.get_road()):
                    continue
                # Exclude rocks from every pathfinding
                if neighbor.get_building() and neighbor.get_building().get_build_type() in [BuildingTypes.ROCK, BuildingTypes.BIG_ROCK]:
                    continue

                # Insert into array if not existing
                try:
                    temp = g_score[neighbor]
                except KeyError:
                    g_score[neighbor] = 1000000
                    f_score[neighbor] = 1000000

                if current.get_road() and neighbor.get_road():
                    tentative_gscore = g_score[current] + 1
                else:
                    if buildable_or_road:
                        tentative_gscore = g_score[current] + 1
                    else:
                        tentative_gscore = g_score[current] + 100

                if tentative_gscore < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_gscore
                    f_score[neighbor] = tentative_gscore + _estimate_distance(neighbor)

                    if neighbor not in open_set:
                        open_set.append(neighbor)

        return []
