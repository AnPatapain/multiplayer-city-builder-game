from class_types.buildind_types import BuildingTypes
from game.utils import generate_uid

class Buildings:
    # all buildings are listed in this class
    def __init__(self, max_occupants, building_size : tuple, building_type: BuildingTypes):
        ### need to add : Risk, current occupants
        self.id = generate_uid()
        self.max_occupants = max_occupants
        self.building_size = building_size
        self.building_type = building_type
        self.number_citizen = 0
        
        #The building haven't problems at creation
        self.is_on_fire = False
        self.is_destroyed = False

    def add_citizen(self,number_citizen):
        self.number_citizen += number_citizen

    def sub_citizen(self,number_citizen):
        self.number_citizen -= number_citizen

    def get_building_type(self):
        return self.building_type

    def get_building_size(self):
        return self.building_size
    