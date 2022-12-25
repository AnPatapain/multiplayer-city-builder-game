from abc import ABC

from buildable.buildable import Buildable
from class_types.buildind_types import BuildingTypes


class Structure(Buildable, ABC):
    def __init__(self, x: int, y: int, build_type: BuildingTypes, build_size: tuple[int, int],
                 max_employee: int):
        super().__init__(x, y, build_type, build_size)

        self.max_employee = max_employee
