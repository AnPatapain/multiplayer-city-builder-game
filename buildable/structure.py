from abc import ABC
from typing import TYPE_CHECKING, Optional
from buildable.buildable import Buildable

if TYPE_CHECKING:
    from class_types.buildind_types import BuildingTypes
    from map_element.tile import Tile


class Structure(Buildable, ABC):
    def __init__(self, x: int, y: int, build_type: 'BuildingTypes',
                 max_employee: int, fire_risk: int, destruction_risk: int):
        super().__init__(x, y, build_type, fire_risk, destruction_risk)
        self.max_employee = max_employee


    def find_adjacent_road(self) -> Optional['Tile']:
        candidates = self.get_adjacent_tiles()

        for candidate in candidates:
            if candidate.get_road():
                return candidate

        return None

    def update_day(self):
        self.risk.risk_progress()
        if self.risk.is_on_fire():
            self.is_on_fire = True
            self.to_ruin()
            return
        if self.risk.is_destroyed():
            self.to_ruin()
            return