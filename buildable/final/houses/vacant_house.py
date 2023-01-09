from buildable.house import House
from class_types.buildind_types import BuildingTypes


class VacantHouse(House):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, BuildingTypes.VACANT_HOUSE, tax=1, desirability=-99, max_citizen=5, prosperity=5,
                         fire_risk=0, destruction_risk=0)

    def is_upgradable(self) -> bool:
        return self.current_citizen > 0

    def conditions_fulfilled(self) -> bool:
        return True

    def upgrade(self):
        #prevent circular import
        from buildable.final.houses.small_tent import SmallTent
        super().upgrade_to(SmallTent)

    def downgrade(self):
        pass