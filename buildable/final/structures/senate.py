from buildable.structure import Structure
from class_types.buildind_types import BuildingTypes
from walkers.final.tax_collector import TaxCollector


class Senate(Structure):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, BuildingTypes.SENATE, max_employee=10, fire_risk=10, destruction_risk=10)

    def new_walker(self):
        if self.associated_walker:
            print("A walker is already assigned to this building!")
            return

        tile = self.find_adjacent_road()
        if tile:
            self.associated_walker = TaxCollector(self)
            self.associated_walker.spawn(tile)

    def update_month(self):
        super().update_month()
        if not self.associated_walker:
            self.new_walker()
    
    def to_ruin(self):
        if self.associated_walker:
            self.associated_walker.delete()
        super().to_ruin()