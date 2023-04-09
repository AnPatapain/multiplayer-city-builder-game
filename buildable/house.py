from abc import ABC, abstractmethod

from buildable.buildable import Buildable
from class_types.buildind_types import BuildingTypes
from game.game_controller import GameController
from walkers.final.immigrant import Immigrant



class House(Buildable, ABC):
    def __init__(self, x: int, y: int, build_type: BuildingTypes,
                 tax: int, desirability: int, max_citizen: int, prosperity: int, fire_risk: int, destruction_risk: int):
        super().__init__(x, y, build_type, fire_risk, destruction_risk)

        self.max_citizen = max_citizen
        self.current_citizen = 0

        self.has_water = False
        self.tax = tax
        self.tax_available = False
        self.happiness = 60
        self.desirability = desirability
        self.prosperity = prosperity

        # Max 5
        self.downgrade_progress: int = 0

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

    def set_has_water(self, has_water):
        self.has_water = has_water

    def get_tax(self):
        return self.tax

    def update_day(self):
        # No update risk if is not your building
        from network_system.system_layer.read_write import SystemInterface
        if self.player_id == SystemInterface.get_instance().get_player_id():
            self.risk.risk_progress()

        if self.risk.is_on_fire():
            self.to_ruin(on_fire=True)
            return

        if not self.conditions_fulfilled():
            if self.downgrade_progress > 5:
                self.downgrade()
                self.downgrade_progress = 0
            else:
                self.downgrade_progress += 1
            return

        # Reset downgrade progress if conditions are fulfilled
        self.downgrade_progress = 0
        if self.is_upgradable():
            self.upgrade()

    def update_happiness(self):
        # it happens once every two weeks
        if GameController.get_instance().get_actual_citizen() < 200:
            self.happiness = 60
        if 200 <= GameController.get_instance().get_actual_citizen() < 300:
            self.happiness = 50


    @abstractmethod
    def is_upgradable(self) -> bool:
        print("FIXME: method is_upgradable is not implemented!")
        return False

    def has_road_in_range(self):
        for adj in self.get_adjacent_tiles(2):
            if adj.get_road():
                return True

        return False

    def conditions_fulfilled(self) -> bool:
        return self.has_road_in_range()

    @abstractmethod
    def upgrade(self):
        pass

    @abstractmethod
    def downgrade(self):
        pass

    def spawn_migrant(self, quantity: int):
        if self.associated_walker or not self.has_road_in_range():
            return

        self.associated_walker = Immigrant(self, self.get_current_tile(), quantity)
        self.associated_walker.spawn(GameController.get_instance().spawn_point)

    def can_accept_new_migrant(self):
        return not self.associated_walker and not self.is_full() and self.has_road_in_range()

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
        # check citizen number
        if self.max_citizen < self.current_citizen:
            self.current_citizen = self.max_citizen
        self.tax = next_object.tax
        self.desirability = next_object.desirability
        self.build_type = next_object.build_type
        self.risk = next_object.risk
        self.__class__ = class_name

    def to_ruin(self, on_fire: bool = False):
        if self.associated_walker:
            self.associated_walker.delete()
        super().to_ruin(on_fire=on_fire)

    def get_has_taxes(self):
        return self.tax_available

    def set_has_taxes(self, value: bool):
        self.tax_available = value
