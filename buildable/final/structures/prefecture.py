from buildable.structure import Structure
from class_types.buildind_types import BuildingTypes


class Prefecture(Structure):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, BuildingTypes.PREFECTURE, build_size=(1, 1), max_employee=6)
