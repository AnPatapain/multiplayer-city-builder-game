from buildable.structure import Structure
from class_types.buildind_types import BuildingTypes

class WheatFarm(Structure):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, BuildingTypes.WHEAT_FARM, build_size=(3, 3), max_employee=10)
    
