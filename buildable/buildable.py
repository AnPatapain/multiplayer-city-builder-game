from abc import ABC
from typing import Optional, TYPE_CHECKING

from buildable.buildable_datas import buildable_size
from events.risk import Risk
from game.game_controller import GameController
from game.setting import GRID_SIZE
from game.textures import Textures

if TYPE_CHECKING:
    from class_types.buildind_types import BuildingTypes
    from walkers.walker import Walker
    from map_element.tile import Tile


class Buildable(ABC):
    def __init__(self, x: int, y: int, build_type: 'BuildingTypes', fire_risk: int, destruction_risk: int):
        self.build_type = build_type

        self.associated_walker: Optional['Walker'] = None

        self.x = x
        self.y = y

        self.risk = Risk(fire_risk, destruction_risk)
        self.count = 0

        self.is_on_fire = False

    def get_current_tile(self) -> 'Tile':
        grid = GameController.get_instance().get_map()
        return grid[self.x][self.y]

    def is_destroyable(self):
        return True

    def get_texture(self):
        return Textures.get_texture(self.build_type, texture_number=self.get_current_tile().random_texture_number)

    def get_delete_texture(self):
        return Textures.get_delete_texture(self.build_type, texture_number=self.get_current_tile().random_texture_number)

    def get_build_texture(self):
        return self.get_texture()

    def get_building_size(self):
        return buildable_size[self.build_type]

    def get_build_type(self):
        return self.build_type

    def on_build_action(self):
        print("FIXME: method on_build_action not implemented!")
        pass

    def destroy(self):
        if self.associated_walker:
            self.associated_walker.delete()
        pass

    def new_walker(self):
        print("FIXME: method new_walker not implemented!")
        pass

    def update_tick(self):
        pass

    def update_day(self):
        pass

    def upgrade(self):
        pass

    def get_adjacent_tiles(self, radius: int = 0):
        build_size = self.get_building_size()

        tiles = set()
        excluded_tiles = set()
        grid = GameController.get_instance().get_map()
        base_tile = self.get_current_tile()
        base_x, base_y = base_tile.x, base_tile.y

        for x in range(build_size[0]):
            for y in range(build_size[1]):
                if base_x - x < 0 or base_y + y > GRID_SIZE:
                    continue

                current_tile = grid[base_x - x][base_y + y]
                excluded_tiles.add(current_tile)
                tiles.update(current_tile.get_adjacente_tiles(radius))

        tiles.difference_update(excluded_tiles)
        return list(tiles)

    def upgrade_to(self, class_name):
        """
            Copied from buidable/house.py
            Testing if we can update wheat_soil using this method
        """
        next_object = class_name(self.x, self.y)
        self.build_type = next_object.build_type
        self.__class__ = class_name

    def to_ruin(self):
        from buildable.final.buildable.ruin import Ruin
        from class_types.buildind_types import BuildingTypes

        grid = GameController.get_instance().get_map()
        build_size = self.get_building_size()

        for x in range(build_size[0]):
            for y in range(build_size[1]):
                tile = grid[self.x - x][self.y + y]
                tile.set_building(Ruin(self.x - x, self.y + y))

    def get_risk(self) -> Risk:
        return self.risk