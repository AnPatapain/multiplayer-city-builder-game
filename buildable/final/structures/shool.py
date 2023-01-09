from buildable.structure import Structure
from class_types.buildind_types import BuildingTypes


class School(Structure):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, BuildingTypes.SCHOOL, build_size=(3,3), max_employee=10, fire_risk=10,
                         destruction_risk=10)