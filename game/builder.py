from game.game_controller import GameController
from class_types.buildind_types import BuildingTypes

from buildable.final.buildable.well import Well
from buildable.final.houses.vacant_house import VacantHouse
from buildable.final.structures.prefecture import Prefecture
from buildable.final.structures.WheatFarm import WheatFarm
from buildable.road import Road

from game.panel import Panel
import game.utils as utils
from game.setting import GRID_SIZE
from map_element.tile import Tile
from class_types.road_types import RoadTypes

class Builder:
    def __init__(self) -> None:
        self.game_controller = GameController.get_instance()

        # Pour construire consécutivement
        self.panel = Panel(1920, 1080)
        self.temp_tile_info: dict = None
        self.start_point: tuple = None
        self.end_point: tuple = None
        self.in_build_action = False

        
    def set_start_point(self, start_point: tuple):
        self.start_point = start_point

    def get_start_point(self): return self.start_point

    def set_end_point(self, end_point: tuple):
        self.end_point = end_point

    def get_end_point(self): return self.end_point

    def set_temp_tile_info(self, temp_tile_info: dict):
        self.temp_tile_info = temp_tile_info

    def get_temp_tile_info(self): return self.temp_tile_info

    def set_in_build_action(self, in_build_action: bool):
        self.in_build_action = in_build_action
    
    def get_in_build_action(self): return self.in_build_action

    def build_from_start_to_end(self, selected_tile, start_point, end_point):
        grid = self.game_controller.get_map()

        if selected_tile == RoadTypes.TL_TO_BR:
            start = grid[start_point[1]][start_point[0]]
            if not start.is_buildable() and not start.get_road():
                return
            end = grid[end_point[1]][end_point[0]]
            if not end.is_buildable() and not end.get_road():
                return
            path = start.find_path_to(end, buildable_or_road=True)

            if path:
                for tile in path:
                    if tile.is_buildable():
                        self.road_add(tile.x, tile.y)

            self.start_point = None  # update start point to default after building
            self.end_point = None  # update start point to default after building
            return

        
        for row in utils.MyRange(start_point[1], end_point[1]):
            for col in utils.MyRange(start_point[0], end_point[0]):
                tile: Tile = grid[row][col]

                if selected_tile == BuildingTypes.PELLE:
                    if tile.is_destroyable():
                        if tile.get_road():
                            tile.destroy()
                            self.road_update(row, col)
                        tile.destroy()
                    continue

                if not tile.is_buildable():
                    continue


                self.building_add(row, col, selected_tile)

                self.start_point = None  # update start point to default after building
                self.end_point = None  # update start point to default after building

    def building_add(self, row, col, selected_type):
        if not self.game_controller.has_enough_denier(selected_type):
            return

        building = None
        match selected_type:
            case BuildingTypes.VACANT_HOUSE:
                building = VacantHouse(row, col)
            case BuildingTypes.PREFECTURE:
                building = Prefecture(row, col)
            case BuildingTypes.WELL:
                building = Well(row, col)
            case BuildingTypes.WHEAT_FARM:
                building = WheatFarm(row, col)
            case BuildingTypes.GRANARY:
                pass
            case BuildingTypes.MARKET:
                pass
            case _:
                print("Building type error")
                return

        grid = self.game_controller.get_map()
        if sum(building.get_building_size()) > 2:
            (x_building, y_building) = building.get_building_size()
            #check if all case are buildable
            try:
                for x in range(col,col+x_building, 1):
                    for y in range(row,row-y_building, -1):
                        if not grid[y][x].is_buildable():
                            print("Building can't be construct")
                            return
            except IndexError:
                #We are out of the index of the grid
                return

            # Put building in each case
            for x in range(col,col+x_building,1):
                for y in range(row,row-y_building,-1):
                    if x != col or y != row:
                        grid[y][x].set_building(building, show_building=False)

        #Show first case
        grid[row][col].set_building(building, show_building=True)
        self.game_controller.new_building(building)

    

    def road_add(self, road_row, road_col):
        """
        DESCRIPTION : Make a new road with connection between other road
        """
        # Create road
        road = Road([])
        road_connection = [None, None, None, None]

        grid = self.game_controller.get_map()
        # Connect other road:
        # TL connection
        if road_col > 0:
            r1 = grid[road_row][road_col - 1].get_road()
            if r1:
                r1.set_connect(road, 2)
                road_connection[0] = r1

        # TR connection
        if road_row > 0:
            r2 = grid[road_row - 1][road_col].get_road()
            if r2:
                r2.set_connect(road, 3)
                road_connection[1] = r2

        # BR connection
        if road_col < GRID_SIZE - 1:
            r3 = grid[road_row][road_col + 1].get_road()
            if r3:
                r3.set_connect(road, 0)
                road_connection[2] = r3

        # BL connection
        if road_row < GRID_SIZE - 1:
            r4 = grid[road_row + 1][road_col].get_road()
            if r4:
                r4.set_connect(road, 1)
                road_connection[3] = r4

        road.set_road_connection(road_connection)
        grid[road_row][road_col].set_road(road)



    def road_update(self, road_row, road_col):
        grid = self.game_controller.get_map()
        if road_col > 0:
            if grid[road_row][road_col - 1].get_road():
                grid[road_row][road_col - 1].get_road().set_connect(grid[road_row][road_col].get_road(), 2)


        # TR connection
        if road_row > 0:
            if grid[road_row - 1][road_col].get_road():
                grid[road_row - 1][road_col].get_road().set_connect(grid[road_row][road_col].get_road(), 3)

        # BR connection
        if road_col < GRID_SIZE - 1:
            if grid[road_row][road_col + 1].get_road():
                grid[road_row][road_col + 1].get_road().set_connect(grid[road_row][road_col].get_road(), 0)

        # BL connection
        if road_row < GRID_SIZE - 1:
            if grid[road_row + 1][road_col].get_road():
                grid[road_row + 1][road_col].get_road().set_connect(grid[road_row][road_col].get_road(), 1)
