from abc import ABC

from buildable.buildable import Buildable
from class_types.buildind_types import BuildingTypes

class House(Buildable, ABC):
        def __init__(self, x: int, y: int, build_type: BuildingTypes, build_size: tuple[int, int],
                     tax: int, desirability: int, max_citizen: int, prosperity: int):
            super().__init__(x, y, build_type, build_size)
            self.max_citizen = max_citizen
            self.current_citizen = 0

            self.has_water = False
            self.tax = tax
            self.desirability = desirability
            self.prosperity = prosperity

        def add_citizen(self, num: int):
            self.current_citizen += num

        def get_citizen(self):
            return self.current_citizen

        def get_max_citizen(self):
            return self.max_citizen

        def get_has_water(self):
            return self.has_water

        def set_has_water(self,has_water):
            self.has_water = has_water

        def get_tax(self):
            return self.tax
