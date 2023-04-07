from typing import TypedDict, Optional

from buildable.buildable import Buildable
from buildable.final.structures.engineer_post import EngineerPost
from buildable.final.structures.hospital import Hospital
from buildable.final.structures.market import Market
from buildable.final.structures.senate import Senate
from buildable.final.structures.shool import School
from buildable.final.structures.temple import Temple
from buildable.final.structures.theatre import Theatre
from game.game_controller import GameController
from class_types.buildind_types import BuildingTypes

from buildable.final.buildable.well import Well
from buildable.final.houses.vacant_house import VacantHouse
from buildable.final.structures.prefecture import Prefecture
from buildable.final.structures.WheatFarm import WheatFarm
from buildable.final.structures.granary import Granary
from buildable.road import Road

import game.utils as utils
from game.setting import GRID_SIZE
from map_element.tile import Tile
from class_types.road_types import RoadTypes
from network_system.system_layer.read_write import SystemInterface


class TempTile(TypedDict):
    name: BuildingTypes | RoadTypes
    isometric_coor: list[tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]]
    render_img_coor: tuple[int, int]
    isBuildable: bool
    isDestroyable: bool

class Builder:
    def __init__(self) -> None:
        self.game_controller = GameController.get_instance()

        self.temp_tile_info: Optional[TempTile] = None
        self.start_point: Optional[tuple[int, int]] = None
        self.end_point: Optional[tuple[int, int]] = None
        self.in_build_action = False

        
    def set_start_point(self, start_point: Optional[tuple[int, int]]):
        self.start_point = start_point

    def get_start_point(self): return self.start_point

    def set_end_point(self, end_point: Optional[tuple[int, int]]):
        self.end_point = end_point

    def get_end_point(self): return self.end_point

    def set_temp_tile_info(self, temp_tile_info: Optional[TempTile]):
        self.temp_tile_info = temp_tile_info

    def get_temp_tile_info(self) -> TempTile:
        return self.temp_tile_info

    def set_in_build_action(self, in_build_action: bool):
        self.in_build_action = in_build_action
    
    def get_in_build_action(self): return self.in_build_action

    def build_from_start_to_end(self, selected_tile: BuildingTypes | RoadTypes, start_point: tuple[int, int], end_point: tuple[int, int]):
        grid = self.game_controller.get_map()

        if selected_tile == RoadTypes.TL_TO_BR:
            start = grid[start_point[1]][start_point[0]]
            if not start.is_buildable() and not start.get_road():
                return
            end = grid[end_point[1]][end_point[0]]
            if not end.is_buildable() and not end.get_road():
                return
            path = start.find_path_to([end], buildable_or_road=True)

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
                        if tile.get_building():
                            self.delete_building(tile.get_building())
                        else:
                            tile.destroy()
                            self.road_update(row, col)
                        self.game_controller.denier -= 2
                    continue

                if not tile.is_buildable():
                    continue


                self.building_add(row, col, selected_tile)

                self.start_point = None  # update start point to default after building
                self.end_point = None  # update start point to default after building


        si = SystemInterface.get_instance()
        si.send_build(start_point, end_point, selected_tile)

    def delete_building(self, tile_with_building: 'Buildable'):
        for tile in tile_with_building.get_all_building_tiles():
            tile.destroy()

    def building_add(self, row: int, col: int, selected_type: RoadTypes | BuildingTypes):
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
                building = Granary(row, col)
            case BuildingTypes.MARKET:
                building = Market(row, col)
            case BuildingTypes.ENGINEERS_POST:
                building = EngineerPost(row,col)
            case BuildingTypes.HOSPITAL:
                building = Hospital(row,col)
            case BuildingTypes.THEATRE:
                building = Theatre(row, col)
            case BuildingTypes.SCHOOL:
                building = School(row, col)
            case BuildingTypes.SENATE:
                if self.game_controller.map_has_senate():
                    print("Senate already present!")
                    return
                building = Senate(row, col)
            case BuildingTypes.TEMPLE:
                building = Temple(row, col)
            case _:
                print("Building type error")
                return

        grid = self.game_controller.get_map()

        if not grid[row][col].is_buildable(building.get_building_size()):
            print("Building can't be constructed")
            return
        
        if building.get_build_type() is BuildingTypes.WHEAT_FARM:
            if not grid[row][col].is_buildable_for_farm(building.get_building_size()):
                print("Farm can't be constructed")
                return 

        if sum(building.get_building_size()) > 2:
            (x_building, y_building) = building.get_building_size()

            # Put building in each case
            for x in range(col,col+x_building,1):
                for y in range(row,row-y_building,-1):
                    if x != col or y != row:
                        grid[y][x].set_building(building, show_building=False)

        #Show first case
        grid[row][col].set_building(building, show_building=True)
        self.game_controller.new_building(building)

    

    def road_add(self, road_row: int, road_col: int):
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


    def road_update(self, road_row: int, road_col: int):
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
