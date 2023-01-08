from buildable.structure import Structure
from class_types.buildind_types import BuildingTypes
from walkers.final.engineer import Engineer


class EngineerPost(Structure):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, BuildingTypes.ENGINEERS_POST, build_size=(1, 1), max_employee=6, fire_risk=20,
                         destruction_risk=0)

    def new_walker(self):
        if self.associated_walker:
            print("A walker is already assigned to this building!")
            return

        tile = self.find_adjacent_road()
        if tile:
            self.associated_walker = Engineer(self)
            self.associated_walker.spawn(tile)

    def update_day(self):
        super().update_day()
        if not self.associated_walker:
            self.new_walker()

    def to_ruin(self):
        if self.associated_walker:
            self.associated_walker.delete()
        super().to_ruin()