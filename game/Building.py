import random as rd
import string as st
import enum
from class_types.buildind_types import TypeBuilding

def ID():
    Id = ''.join([rd.choice(st.ascii_letters + st.digits) for n in range(5)])
    return Id

class typeBuilding(enum):
    SMALL_TENT = 1
    LARGE_TENT = 2
    SMALL_SHACK = 3
    LARGE_SHACK = 4
    SENATE = 11
    ENGINEERS_POST = 12
    PREFECTURE = 13
    WELL = 20
    FOUNTAIN = 21
    

class Buildings():
    # all buildings are listed in this class
    def __init__(self, max_occupants, building_size, cost, typeBuilding):
        ### need to add : Risk, current occupants
        self.id = ID()
        self.max_occupants = max_occupants
        self.building_size = building_size
        self.cost = cost
        self.typeBuilding = typeBuilding
        
        #The building haven't problems at creation
        self.IsOnFire = False
        self.IsDestroyed = False

