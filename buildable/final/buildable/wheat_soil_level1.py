from buildable.buildable import Buildable
from class_types.buildind_types import BuildingTypes


class Wheat_soil_level_1(Buildable):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, BuildingTypes.WHEAT_SOIL_LEVEL_1, (1, 1))