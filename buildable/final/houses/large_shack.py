from buildable.house import House
from class_types.buildind_types import BuildingTypes


class LargeShack(House):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, BuildingTypes.SMALL_TENT, build_size=(1, 1),
                         tax=1, desirability=-99, max_citizen=5, prosperity=5)

    def is_upgradable(self) -> bool:
        return False

    def conditions_fulfilled(self) -> bool:
        #TODO : temple gestion
        return True