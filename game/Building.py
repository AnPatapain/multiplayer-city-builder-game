import random as rd
import string as st
from class_types.buildind_types import TypeBuilding

def ID():
    Id = ''.join([rd.choice(st.ascii_letters + st.digits) for n in range(5)])
    return Id

class Buildings():
    # all buildings are listed in this class
    def __init__(self, max_occupants, building_size, cost, typeBuilding : TypeBuilding):
        ### need to add : Risk, current occupants
        self.id = ID()
        self.max_occupants = max_occupants
        self.building_size = building_size
        self.cost = cost
        self.typeBuilding = typeBuilding
        
        #The building haven't problems at creation
        self.IsOnFire = False
        self.IsDestroyed = False

