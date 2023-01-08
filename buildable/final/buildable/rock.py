from buildable.buildable import Buildable
from class_types.tile_types import TileTypes
from game.textures import Textures


class Rock(Buildable):
    def __init__(self, x: int, y: int, taille : tuple = (1, 1)):
        super().__init__(x, y, TileTypes.ROCK, taille, fire_risk=0,destruction_risk=0)

    def is_destroyable(self):
        return False
    