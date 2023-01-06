from buildable.buildable import Buildable
from class_types.buildind_types import BuildingTypes
from game.textures import Textures


class Ruin(Buildable):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, BuildingTypes.RUINS, (1, 1), 0, 0)

    def is_destroyable(self):
        return not self.is_on_fire

    def update_day(self):
        if self.is_on_fire:
            self.count += 1
            if self.count > 3:
                self.is_on_fire = False

    def get_texture(self):
        if self.is_on_fire:
            return Textures.get_texture(BuildingTypes.FIRE_RUINS)
        else:
            return Textures.get_texture(BuildingTypes.RUINS)

