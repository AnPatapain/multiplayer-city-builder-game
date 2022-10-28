import random as rd
import string as st

def ID():
    Id = ''.join([rd.choice(st.ascii_letters + st.digits) for n in range(5)])
    return Id

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


    """
    class ServiceBuilding(Buildings):
    # insert here (prefecture + structure ingenieurs)
    class Water_struct(Buildings):
        def __init__(self, max_occupants, building_size, cost, IsOnFire, IsDestroyed, Labor):
            Buildings.__init__(self, max_occupants, building_size, cost, IsOnFire, IsDestroyed)
            self.Labor = Labor
            bui_Well = (0, '1x1', 5, False, False, False, False)
            bui_Fountain = (0, '2x2', 15, False, False, False, 4)
    """





##road =4, well = 5, clearland=2, engineer = 30, prefecture =30,fountain= 15, reservoire=80, aqueduct=8


### water levels doc :  -False = not allowed; 1=Well allowed; 2 = ONLY the fountain is allowed ; 3 = Both Well and Fountain are allowed