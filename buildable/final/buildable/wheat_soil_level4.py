from buildable.buildable import Buildable
from class_types.buildind_types import BuildingTypes


class Wheat_soil_level_4(Buildable):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, BuildingTypes.WHEAT_SOIL_LEVEL_4, (1, 1))

    def upgrade(self):
        '''Copy idea from buildable/final/houses/vacant_house.py'''
        from buildable.final.buildable.wheat_soil_level5 import Wheat_soil_level_5
        super().upgrade_to(Wheat_soil_level_5)