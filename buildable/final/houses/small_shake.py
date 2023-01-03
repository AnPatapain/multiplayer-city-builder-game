from buildable.house import House
from class_types.buildind_types import BuildingTypes


class SmallShake(House):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, BuildingTypes.SMALL_TENT, build_size=(1, 1),
                         tax=1, desirability=-5, max_citizen=9, prosperity=15)

    def is_upgradable(self) -> bool:
        #TODO : Add temple and get if map have any temple
        print("FIXME : add temple in map")
        return True

    def conditions_fulfilled(self) -> bool:
        return super().max_citizen > 9