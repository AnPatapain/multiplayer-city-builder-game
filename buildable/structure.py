from abc import ABC
from typing import TYPE_CHECKING, Optional

from buildable.buildable import Buildable
from class_types.buildind_types import BuildingTypes
from game.gameController import GameController

if TYPE_CHECKING:
    from map_element.tile import Tile


class Structure(Buildable, ABC):
    def __init__(self, x: int, y: int, build_type: BuildingTypes, build_size: tuple[int, int],
                 max_employee: int):
        super().__init__(x, y, build_type, build_size)

        self.max_employee = max_employee

    def find_adjacent_road(self) -> Optional['Tile']:
        gc = GameController.get_instance()

        if self.x >= 1:
            tile = gc.get_map()[self.x-1][self.y]
            if tile.get_road():
                return tile

        if self.x < 50:
            tile = gc.get_map()[self.x+1][self.y]
            if tile.get_road():
                return tile

        if self.y< 50:
            tile = gc.get_map()[self.x][self.y+1]
            if tile.get_road():
                return tile

        if self.y >= 1:
            tile = gc.get_map()[self.x][self.y-1]
            if tile.get_road():
                return tile

        return None
