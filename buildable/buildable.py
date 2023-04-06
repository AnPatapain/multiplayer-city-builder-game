from abc import ABC
from typing import Optional, TYPE_CHECKING

import pygame

from game.id import ID_GEN
from buildable.buildable_datas import buildable_size
from events.risk import Risk
from game.game_controller import GameController
from game.textures import Textures

if TYPE_CHECKING:
    from class_types.buildind_types import BuildingTypes
    from walkers.walker import Walker
    from map_element.tile import Tile


class Buildable(ABC):
    def __init__(self, x: int, y: int, build_type: 'BuildingTypes', fire_risk: int, destruction_risk: int, desirability:int =0, player_id: int = 0, id: int =0):
        self.build_type = build_type

        self.associated_walker: Optional['Walker'] = None

        self.x = x
        self.y = y
        self.desirability = desirability
        self.risk = Risk(fire_risk, destruction_risk)
        self.count = 0
        self.player_id = player_id

        id_create = ID_GEN()
        self.id = id_create.id_gen()
        self.is_on_fire = False

    def get_all_building_tiles(self) -> list['Tile']:
        grid = GameController.get_instance().get_map()
        build_size = self.get_building_size()

        tiles = []
        for x in range(build_size[0]):
            for y in range(build_size[1]):
                tiles.append(grid[self.x - x][self.y + y])

        return tiles

    def get_current_tile(self)-> 'Tile':
        grid = GameController.get_instance().get_map()
        return grid[self.x][self.y]

    def get_desirability(self):
        return self.desirability

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

    def update_desirability(self):
        pass

    def upgrade(self):
        pass

    def get_adjacent_tiles(self, radius: int = 0):
        tiles = set()
        excluded_tiles = set()

        for current_tile in self.get_all_building_tiles():
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

    def to_ruin(self, on_fire: bool = False):
        from buildable.final.buildable.ruin import Ruin

        for tile in self.get_all_building_tiles():
            tile.set_building(Ruin(tile.x, tile.y))
            tile.get_building().is_on_fire = on_fire

        if on_fire:
            feu = pygame.mixer.Sound('sounds/wavs/burning_ruin.wav')
            feu.play()
        else:
            ecoulement = pygame.mixer.Sound('sounds/wavs/EXPLOD1.WAV')
            ecoulement.play()

    def get_risk(self) -> Risk:
        return self.risk
