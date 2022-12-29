from buildable.buildable import Buildable
from class_types.tile_types import TileTypes


class Rock(Buildable):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, TileTypes.ROCK, (1, 1))

    def is_destroyable(self):
        return False
    