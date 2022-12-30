from abc import ABC

from class_types.buildind_types import BuildingTypes
from game.textures import Textures


class Buildable(ABC):
    def __init__(self, x: int, y: int, build_type: BuildingTypes, build_size: tuple[int, int]):
        self.build_type = build_type
        self.build_size = build_size

        self.x = x
        self.y = y

        self.is_on_fire = False

    def is_destroyable(self):
        return True

    def get_texture(self):
        return Textures.get_texture(self.build_type)

    def get_delete_texture(self):
        return Textures.get_delete_texture(self.build_type)

    def get_build_texture(self):
        return self.get_texture()

    def get_building_size(self):
        return self.build_size

    def get_build_type(self):
        return self.build_type
