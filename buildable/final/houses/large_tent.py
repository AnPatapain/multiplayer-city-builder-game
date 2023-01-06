from buildable.house import House
from class_types.buildind_types import BuildingTypes


class LargeTent(House):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, BuildingTypes.LARGE_TENT, build_size=(1, 1),
                         tax=1, desirability=0, max_citizen=11, prosperity=20)

    def is_upgradable(self) -> bool:
        return self.is_full()
        #TODO : Food
        return False

    def conditions_fulfilled(self) -> bool:
        return self.get_current_tile().get_water_access()

    def upgrade(self):
        # Prevent circular import
        from buildable.final.houses.small_shack import SmallShack
        super().upgrade_to(SmallShack)

    def downgrade(self):
        #Prevent circular import
        from buildable.final.houses.small_tent import SmallTent
        super().upgrade_to(SmallTent)