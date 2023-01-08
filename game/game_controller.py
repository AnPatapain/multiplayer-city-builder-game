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

        self.spawn_point: 'Tile' = None
        self.leave_point: 'Tile' = None

        self.current_tick = 0
        self.current_day = 0
        self.current_month = 0
        self.current_year = 340
        self.total_day = 0

        self.current_speed = 1.0

        # Not implemented yet
        self.sentiment = 80
        self.months = {
            0: "Jan", 1: "Feb", 2: "Mar", 3: "Apr", 4: "May", 5: "Jun", 6: "Jul", 7: "Aug", 8: "Sep", 9: "Oct",
            10: "Nov", 11: "Dec"
        }

    def get_current_speed(self):
        return self.current_speed

    def increase_current_speed(self):
        if self.current_speed != 8.0:
            self.current_speed *= 2

    def decrease_current_speed(self):
        if self.current_speed != 0.5:
            self.current_speed /= 2

    def get_month(self, id: int):
        return self.months[id]

    def get_actual_citizen(self):
        return self.actual_citizen

    def get_actual_month(self):
        return self.current_month

    def get_actual_year(self):
        return self.current_year

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

    def update(self):
        self.increase_tick()

    def increase_tick(self):
        if self.current_tick == 50:
            self.increase_day()
            self.current_tick = -1

        self.current_tick += 1

        match self.current_tick:
            case 0:
                self.__calculate_water_access()
            case 1:
                self.__migration_update()
            case 2:
                self.__calculate_actual_citizen()


    def increase_day(self):
        if self.current_day == 15:
            self.increase_month()
            self.current_day = -1

        for row in self.grid:
            for tile in row:
                building = tile.get_building()
                if building:
                    building.update_day()

        self.current_day += 1

    def increase_month(self):
        if self.current_month == 11:
            self.increase_year()
            self.current_month = -1
        self.current_month += 1


    def increase_year(self):
        self.current_year -= 1

    def __calculate_actual_citizen(self):
        from buildable.house import House
        self.actual_citizen = 0
        for row in self.grid:
            for tile in row:
                building = tile.get_building()
                if building and isinstance(building,House):
                    self.actual_citizen += int(building.get_citizen())

    def __calculate_water_access(self):
        wells = []
        # Set everything to 0, and list wells
        for row in self.grid:
            for tile in row:
                tile.set_water_access(False)
                if tile.get_building() and tile.get_building().build_type == BuildingTypes.WELL:
                    wells.append(tile)

        # Put water around each wells
        for well in wells:
            for tile in well.get_adjacente_tiles(2):
                tile.set_water_access(True)

    def __migration_update(self):
        from buildable.house import House

        migrant_ammount = self.sentiment * 12 / 100

        for row in self.grid:
            for tile in row:
                if migrant_ammount <= 0:
                    return
                building = tile.get_building()
                if building and isinstance(building, House):
                    house: House = building
                    if not house.associated_walker and not house.is_full():
                        if migrant_ammount <= 4:
                            if house.empty_space() < migrant_ammount:
                                house.spawn_migrant(house.empty_space())
                                migrant_ammount -= house.empty_space()
                            else:
                                house.spawn_migrant(migrant_ammount)
                                migrant_ammount = 0
                        else:
                            if house.empty_space() < 4:
                                house.spawn_migrant(house.empty_space())
                                migrant_ammount -= house.empty_space()
                            else:
                                house.spawn_migrant(4)
                                migrant_ammount -= 4


    @staticmethod
    def get_instance():
        if GameController.instance is None:
            GameController.instance = GameController()
        return GameController.instance
