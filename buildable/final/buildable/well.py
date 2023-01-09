from buildable.buildable import Buildable
from class_types.buildind_types import BuildingTypes


class Well(Buildable):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, BuildingTypes.WELL, fire_risk=0, destruction_risk=0)
