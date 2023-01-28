from random import randint

from buildable.buildable import Buildable
from class_types.buildind_types import BuildingTypes
from game.textures import Textures


class Ruin(Buildable):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, BuildingTypes.RUINS, fire_risk=0, destruction_risk=0)

        self.ruin_type = randint(0, 4)
        self.animation = 0

    def is_destroyable(self):
        return not self.is_on_fire

    def update_tick(self):
        if self.is_on_fire:
            self.animation += 0.4

    def update_day(self):
        if self.is_on_fire:
            self.count += 1
            if self.count > 10:
                self.is_on_fire = False

    def get_texture_index(self):
        if self.is_on_fire:
            return self.ruin_type * 8 + int(self.animation % 8)
        else:
            return self.ruin_type

    def get_texture(self):
        if self.is_on_fire:
            return Textures.get_texture(BuildingTypes.FIRE_RUINS, self.get_texture_index())
        else:
            return Textures.get_texture(BuildingTypes.RUINS, self.ruin_type)


    def get_delete_texture(self):
        return Textures.get_delete_texture(BuildingTypes.RUINS, self.ruin_type)
