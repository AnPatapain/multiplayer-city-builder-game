from typing import TYPE_CHECKING

from class_types.buildind_types import BuildingTypes
from buildable.buildableCost import buildable_cost

if TYPE_CHECKING:
    from walkers.walker import Walker
    from map_element.tile import Tile
    from buildable.buildable import Buildable


class GameController:
    instance = None

    def __init__(self):
        self.grid: list[list['Tile']] = None
        self.denier = 100000
        self.actual_citizen = 0
        self.max_citizen = 0
        self.walkers: list['Walker'] = []


    def new_building(self, building: 'Buildable'):
        self.denier -= buildable_cost[building.get_build_type()]
        building.on_build_action()

    def has_enough_denier(self, building_type: 'BuildingTypes'):
        return buildable_cost[building_type] <= self.denier

    def get_denier(self):
        return self.denier

    def set_map(self, map):
        self.grid = map

    def get_map(self) -> list[list['Tile']]:
        return self.grid

    def add_walker(self, walker: 'Walker'):
        self.walkers.append(walker)

    def remove_walker(self, walker: 'Walker'):
        self.walkers.remove(walker)

    @staticmethod
    def get_instance():
        if GameController.instance is None:
            GameController.instance = GameController()
        return GameController.instance
