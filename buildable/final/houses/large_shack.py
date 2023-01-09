from buildable.house import House
from class_types.buildind_types import BuildingTypes


class LargeShack(House):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, BuildingTypes.LARGE_SHACK, tax=1, desirability=-99, max_citizen=5, prosperity=5,
                         fire_risk=0, destruction_risk=0)

    def is_upgradable(self) -> bool:
        return False

    def conditions_fulfilled(self) -> bool:
        #TODO : temple gestion
        return False

    def upgrade(self):
        pass

    def downgrade(self):
        from buildable.final.houses.small_shack import SmallShack
        super().upgrade_to(SmallShack)
