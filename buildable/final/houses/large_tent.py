from buildable.final.houses.small_shack import SmallShack
from buildable.house import House
from class_types.buildind_types import BuildingTypes


class LargeTent(House):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, BuildingTypes.LARGE_TENT, build_size=(1, 1),
                         tax=1, desirability=0, max_citizen=11, prosperity=20)

    def is_upgradable(self) -> bool:
        return True

    def conditions_fulfilled(self) -> bool:
        return True

    def upgrade(self):
        super().upgrade_to(SmallShack)