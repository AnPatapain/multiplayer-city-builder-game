from abc import ABC, abstractmethod

from buildable.buildable import Buildable
from buildable.final.buildable.ruin import Ruin
from class_types.buildind_types import BuildingTypes
from game.game_controller import GameController
from walkers.final.immigrant import Immigrant


class House(Buildable, ABC):
    def __init__(self, x: int, y: int, build_type: BuildingTypes, build_size: tuple[int, int],
                 tax: int, desirability: int, max_citizen: int, prosperity: int,fire_risk : int ,destruction_risk: int):
        super().__init__(x, y, build_type,build_size,fire_risk ,destruction_risk)


        self.max_citizen = max_citizen
        self.current_citizen = 0

        self.has_water = False
        self.tax = tax
        self.desirability = desirability
        self.prosperity = prosperity

    def is_full(self) -> bool:
        return self.current_citizen >= self.max_citizen

    def empty_space(self) -> int:
        return self.max_citizen - self.current_citizen

    def add_citizen(self, num: int):
        self.current_citizen += num

    def get_citizen(self):
        return self.current_citizen

    def get_max_citizen(self):
        return self.max_citizen

    def get_has_water(self):
        return self.has_water

    def set_has_water(self,has_water):
        self.has_water = has_water

    def get_tax(self):
        return self.tax

    def update_day(self):
        self.risk.risk_progress()

        if self.risk.is_on_fire():
            self.is_on_fire = True
            self.to_ruin()
            return

        if not self.conditions_fulfilled():
            self.downgrade()
        if self.is_upgradable():
            print("hehe")
            self.upgrade()

    @abstractmethod
    def is_upgradable(self) -> bool:
        print("FIXME: method is_upgradable is not implemented!")
        return False

    @abstractmethod
    def conditions_fulfilled(self) -> bool:
        print("FIXME: method conditions_fulfilled is not implemented!")
        return True

    @abstractmethod
    def upgrade(self):
        pass

    @abstractmethod
    def downgrade(self):
        pass

    def spawn_migrant(self, quantity: int):
        if self.associated_walker:
            return

        self.associated_walker = Immigrant(self, self.get_current_tile(), quantity)
        self.associated_walker.spawn(GameController.get_instance().spawn_point)

    def upgrade_to(self, class_name):
        """
            House auto upgrade (testing)
            Change element:
                - max_citizen
                - tax
                - desirability
                - build_type
                - Risk
            No change element:
                - has_water
                - current_citizen
                - position(x,y)
                - build_size
                - is_on_fire
        """
        next_object = class_name(self.x, self.y)
        self.max_citizen = next_object.max_citizen
        #check citizen number
        if self.max_citizen < self.current_citizen:
                self.current_citizen = self.max_citizen
        self.tax = next_object.tax
        self.desirability = next_object.desirability
        self.build_type = next_object.build_type
        self.risk = next_object.risk
        self.__class__ = class_name

    def to_ruin(self):
        if self.associated_walker:
            self.associated_walker.delete()
        super().to_ruin()