from abc import ABC
from typing import Optional, TYPE_CHECKING

from game.textures import Textures

if TYPE_CHECKING:
    from class_types.buildind_types import BuildingTypes
    from walkers.walker import Walker


class Buildable(ABC):
    def __init__(self, x: int, y: int, build_type: 'BuildingTypes', build_size: tuple[int, int]):
        self.build_type = build_type
        self.build_size = build_size

        self.associated_walker: Optional[Walker] = None

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

    def destroy(self):
        print("FIXME: method destroy not implemented!")
        pass

    def new_walker(self):
        print("FIXME: method new_walker not implemented!")
        pass
