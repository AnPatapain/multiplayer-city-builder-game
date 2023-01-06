from buildable.buildable import Buildable
from class_types.tile_types import TileTypes
from game.textures import Textures


class SmallTree(Buildable):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, TileTypes.TREE, (1, 1))
    def get_texture(self):
        return Textures.get_texture(self.build_type)[self.get_current_tile().id_number]