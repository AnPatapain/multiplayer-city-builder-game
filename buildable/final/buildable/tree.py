from buildable.buildable import Buildable
from class_types.buildind_types import BuildingTypes


class SmallTree(Buildable):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, BuildingTypes.TREE, (1, 1),0,0)
