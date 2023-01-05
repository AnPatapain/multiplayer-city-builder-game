from buildable.buildable import Buildable
from class_types.tile_types import TileTypes

class SmallTree(Buildable):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, TileTypes.TREE, (1, 1))
