from buildable.structure import Structure
from class_types.buildind_types import BuildingTypes
from walkers.final.random_walkers.Prefet import Prefet


class Prefecture(Structure):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, BuildingTypes.PREFECTURE, build_size=(1, 1), max_employee=6)
        self.new_walker()

    def new_walker(self):
        if self.associated_walker:
            print("A walker is already assigned to this building!")
            return

        tile = self.find_adjacent_road()
        if tile:
            self.associated_walker = Prefet(self)
            self.associated_walker.spawn(tile)

    def destroy(self):
        if self.associated_walker:
            self.associated_walker.delete()
