from buildable.buildable import Buildable
from class_types.buildind_types import BuildingTypes


class BigRock(Buildable):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, BuildingTypes.BIG_ROCK, fire_risk=0, destruction_risk=0)

    def is_destroyable(self):
        return False
