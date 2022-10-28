from distutils.command.build import build
from taboule_rasa.game.Building import Buildings


from Building import Buildings

class Tiles:
    #miss road
    #Put none 
    def __init__(self,waterAcces : int ,building :Buildings):
        self.building = building
        self.waterAccess = waterAcces
        #Verfication un batiment est dessus
        if (self.building == None):
            self.isOccupied = False
        else :
            self.isOccupied = True

    def putBuilding(self,building : Buildings):
        self.building = building
        self.isOccupied = True

    def removeBuilding(self) :
        self.building = None
        self.isOccupied = False
        