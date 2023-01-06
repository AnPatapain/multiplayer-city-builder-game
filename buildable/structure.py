from abc import ABC
from typing import TYPE_CHECKING, Optional

from buildable.buildable import Buildable
from events.risk import Risk

if TYPE_CHECKING:
    from class_types.buildind_types import BuildingTypes
    from map_element.tile import Tile


class Structure(Buildable, ABC):
    def __init__(self, x: int, y: int, build_type: 'BuildingTypes', build_size: tuple[int, int],
                 max_employee: int,fire_risk : int ,destruction_risk: int):
        super().__init__(x, y, build_type,build_size)

        self.risk = Risk(fire_risk, destruction_risk)

        self.max_employee = max_employee

    def find_adjacent_road(self) -> Optional['Tile']:
        current_tile = self.get_current_tile()
        candidates = current_tile.get_adjacente_tiles()

        for candidate in candidates:
            if candidate.get_road():
                return candidate

        return None

    def update_day(self):
        self.risk.risk_progress()
