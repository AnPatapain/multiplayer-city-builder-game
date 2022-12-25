from buildable.building import Buildings
from class_types.buildind_types import BuildingTypes

class Houses(Buildings):
        def __init__(self, max_occupants, building_size : tuple, has_water, tax, desirability,building_type : BuildingTypes):
            Buildings.__init__(self, max_occupants, building_size, building_type)
            self.has_water = has_water
            self.tax = tax
            self.desirability = desirability

        def get_has_water(self):
            return self.has_water

        def set_has_water(self,has_water):
            self.has_water = has_water

        def get_tax(self):
            return self.tax
