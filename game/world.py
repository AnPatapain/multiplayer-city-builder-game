import pygame as pg
from PIL import Image

import game.utils as utils
from buildable.final.buildable.well import Well
from buildable.final.houses.small_tent import SmallTent
from buildable.final.rock import Rock
from buildable.final.structures.prefecture import Prefecture
from buildable.final.tree import SmallTree
from buildable.road import Road
from class_types.buildind_types import BuildingTypes
from class_types.road_types import RoadTypes
from class_types.tile_types import TileTypes
from events.event_manager import EventManager
from game.game_controller import GameController
from game.map_controller import MapController
from game.setting import *
from game.textures import Textures
from map_element.tile import Tile


class World:

    def __init__(self, nums_grid_x, nums_grid_y, width, height, panel):
        self.game_controller = GameController.get_instance()
        self.nums_grid_x = nums_grid_x
        self.nums_grid_y = nums_grid_y
        self.width = width
        self.height = height

        self.default_surface = pg.Surface((DEFAULT_SURFACE_WIDTH, DEFAULT_SURFACE_HEIGHT)).convert()
        self.game_controller.set_map(self.load_map())
        self.grid = self.game_controller.get_map()


        '''
        create map only once by bliting texture directly on default surface not on screen and then we can blit default surface on screen 
        '''
        self.create_static_map()

        # For building feature
        self.panel = panel
        self.temp_tile = None
        self.start_point = None
        self.end_point = None
        self.in_build_action = False

        #shortcup
        EventManager.register_key_listener(pg.K_h,lambda : self.panel.set_selected_tile(BuildingTypes.SMALL_TENT))
        EventManager.register_key_listener(pg.K_d,lambda : self.panel.set_selected_tile(BuildingTypes.PELLE))
        EventManager.register_key_listener(pg.K_p,lambda : self.panel.set_selected_tile(BuildingTypes.PREFECTURE))
        EventManager.register_key_listener(pg.K_r,lambda : self.panel.set_selected_tile(RoadTypes.TL_TO_BR))
        EventManager.register_key_listener(pg.K_w,lambda : self.panel.set_selected_tile(BuildingTypes.WELL))

    def mouse_pos_to_grid(self, mouse_pos, map_pos):
        """
        DESCRIPTION: Convert position of mouse to row and col on grid. ex: convert (192.15, 30.14) to (row: 40, col: 10)
        To do that we reverse this process: (col, row) -> convert_to_iso -> offset (1/2 default_surface.width, 0) -> offset (map_pos[0], map_pos[1])

        Params: mouse_position: tuple, map_position: tuple

        Return: (col, row) of mouse_position in the grid
        """

        iso_x = mouse_pos[0] - map_pos[0] - self.default_surface.get_width() / 2
        iso_y = mouse_pos[1] - map_pos[1]

        # transform to cart (inverse of cart_to_iso)
        cart_x = (iso_x + 2 * iso_y) / 2
        cart_y = (2 * iso_y - iso_x) / 2

        # transform to grid coordinates
        grid_col = int(cart_x // TILE_SIZE)
        grid_row = int(cart_y // TILE_SIZE)
        return grid_col, grid_row

    def event_handler(self, event, map_pos):

        """
        DESCRIPTION: Handling the events that be gotten from event queue in module event_manager.py

        Params: event retrieved from pg.event.get() in event_manager.py, map_position in map_controller.py

        Return: None
        """

        mouse_pos = pg.mouse.get_pos()
        mouse_grid_pos = self.mouse_pos_to_grid(mouse_pos, map_pos)

        if self.in_map(mouse_grid_pos):
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1 and self.panel.has_selected_tile():
                    self.start_point = mouse_grid_pos
                    self.end_point = mouse_grid_pos
                    self.in_build_action = True

            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 1 and self.panel.has_selected_tile():
                    self.in_build_action = False
                    self.end_point = mouse_grid_pos

            elif event.type == pg.MOUSEMOTION:
                self.end_point = mouse_grid_pos

    def update(self):
        """
        DESCRIPTION: updating the state of the world. For now it updates temp_tile, texture of the world
        
        Return: None
        """
        mouse_pos = pg.mouse.get_pos()
        map_pos = MapController.get_map_pos()
        mouse_grid_pos = self.mouse_pos_to_grid(mouse_pos, map_pos)
        mouse_action = pg.mouse.get_pressed()

        selected_tile = self.panel.get_selected_tile()
        self.temp_tile = None

        if selected_tile:
            if self.in_map(mouse_grid_pos):
                tile = self.grid[mouse_grid_pos[1]][mouse_grid_pos[0]]
                self.temp_tile = {
                    'name': selected_tile,
                    'isometric_coor': tile.get_isometric_coord(),
                    'render_img_coor': tile.get_render_coord(),
                    'isBuildable': tile.is_buildable(),
                    'isDestroyable': tile.is_destroyable()
                }

            # Build from start point to end point
            if not self.in_build_action and self.start_point and self.end_point:
                if self.in_map(self.start_point) and self.in_map(self.end_point):

                    for row in utils.MyRange(self.start_point[1], self.end_point[1]):
                        for col in utils.MyRange(self.start_point[0], self.end_point[0]):
                            tile: Tile = self.grid[row][col]

                            if selected_tile == BuildingTypes.PELLE:
                                if tile.is_destroyable():
                                    if tile.get_road():
                                        tile.destroy()
                                        self.road_update(row, col)
                                    tile.destroy()
                                continue

                            if not tile.is_buildable():
                                continue

                            match selected_tile:
                                case RoadTypes.TL_TO_BR:
                                    self.road_add(row, col)
                                case _:
                                    self.building_add(row, col, selected_tile)

                    self.start_point = None  # update start point to default after building
                    self.end_point = None  # update start point to default after building

            if mouse_action[2]:
                self.panel.set_selected_tile(None)
                self.start_point = None
                self.end_point = None
                self.in_build_action = False

    def draw(self, screen):
        map_pos = MapController.get_map_pos()
        screen.blit(self.default_surface, map_pos)

        for row in self.grid:
            for tile in row:
                (x, y) = tile.get_render_coord()
                (x_offset, y_offset) = (x + self.default_surface.get_width() / 2 + map_pos[0], y + map_pos[1])

                if tile.get_road() or tile.get_building():
                    screen.blit(tile.get_texture(), (x_offset, y_offset - tile.get_texture().get_height() + TILE_SIZE))
                for walker in tile.walkers:
                    screen.blit(walker.get_texture(), (x_offset + TILE_SIZE/2 + walker.walk_progression, y_offset))

        if self.temp_tile and not self.in_build_action:
            isometric_coor = self.temp_tile['isometric_coor']
            isometric_coor_offset = [(x + map_pos[0] + self.default_surface.get_width() / 2, y + map_pos[1]) for x, y in
                                     isometric_coor]

            (x, y) = self.temp_tile['render_img_coor']
            (x_offset, y_offset) = (x + self.default_surface.get_width() / 2 + map_pos[0],
                                    y + map_pos[1])

            texture = Textures.get_texture(self.temp_tile['name'])
            screen.blit(texture, (x_offset, y_offset - texture.get_height() + TILE_SIZE))

            if self.temp_tile['isBuildable']:
                pg.draw.polygon(screen, (0, 255, 0), isometric_coor_offset)
            else:
                pg.draw.polygon(screen, (255, 0, 0), isometric_coor_offset)

        if self.in_build_action:

            if self.in_map(self.start_point) and self.in_map(self.end_point):
                for row in utils.MyRange(self.start_point[1], self.end_point[1]):
                    for col in utils.MyRange(self.start_point[0], self.end_point[0]):

                        (x, y) = self.grid[row][col].get_render_coord()
                        (x_offset, y_offset) = ( x + self.default_surface.get_width() / 2 + map_pos[0], y + map_pos[1] )

                        if self.grid[row][col].is_buildable() and self.temp_tile and self.temp_tile["name"] != BuildingTypes.PELLE:
                            build_sign = Textures.get_texture(BuildingTypes.BUILD_SIGN)
                            screen.blit(build_sign,
                                        (x_offset, y_offset - build_sign.get_height() + TILE_SIZE))

                        elif self.grid[row][col].is_destroyable() and self.temp_tile and self.temp_tile["name"] == BuildingTypes.PELLE:
                            building = self.grid[row][col].get_delete_texture()
                            screen.blit(building,
                                        (x_offset, y_offset - building.get_height() + TILE_SIZE))



    def create_static_map(self):
        for row in self.grid:
            for tile in row:
                tile: Tile = tile
                texture_image = Textures.get_texture(tile.type)
                (x, y) = tile.get_render_coord()
                offset = (x + self.default_surface.get_width() / 2, y - texture_image.get_height() + TILE_SIZE)
                self.default_surface.blit(texture_image, offset)


    def in_map(self, grid_pos):
        """
        DESCRIPTION: Check whether the mouse_grid_pos is in map or not. Ex: our map is 30x30 and mouse_grid_pos is (row: 31, col: 32)
        so the mouse is not in the map

        Params: the grid pos of mouse

        Return: boolean
        """
        mouse_on_panel = False
        in_map_limit = (0 <= grid_pos[0] < self.nums_grid_x) and (0 <= grid_pos[1] < self.nums_grid_y)
        for rect in self.panel.get_panel_rects():
            if rect.collidepoint(pg.mouse.get_pos()):
                mouse_on_panel = True
        return (in_map_limit and not mouse_on_panel)

    def road_add(self, road_row, road_col):
        """
        DESCRIPTION : Make a new road with connection between other road
        """
        # Create road
        road = Road([])
        road_connection = [None, None, None, None]

        # Connect other road:
        # TL connection
        if road_col > 0:
            r1 = self.grid[road_row][road_col - 1].get_road()
            if r1:
                r1.set_connect(road, 2)
                road_connection[0] = r1

        # TR connection
        if road_row > 0:
            r2 = self.grid[road_row - 1][road_col].get_road()
            if r2:
                r2.set_connect(road, 3)
                road_connection[1] = r2

        # BR connection
        if road_col < self.nums_grid_x - 1:
            r3 = self.grid[road_row][road_col + 1].get_road()
            if r3:
                r3.set_connect(road, 0)
                road_connection[2] = r3

        # BL connection
        if road_row < self.nums_grid_y - 1:
            r4 = self.grid[road_row + 1][road_col].get_road()
            if r4:
                r4.set_connect(road, 1)
                road_connection[3] = r4

        road.set_road_connection(road_connection)
        self.grid[road_row][road_col].set_road(road)

    def road_update(self, road_row, road_col):
        if  road_col > 0:
            if self.grid[road_row][road_col - 1].get_road():
                self.grid[road_row][road_col - 1].get_road().set_connect(self.grid[road_row][road_col].get_road(), 2)


        # TR connection
        if road_row > 0:
            if self.grid[road_row - 1][road_col].get_road():
                self.grid[road_row - 1][road_col].get_road().set_connect(self.grid[road_row][road_col].get_road(), 3)

        # BR connection
        if road_col < self.nums_grid_x - 1:
            if self.grid[road_row][road_col + 1].get_road():
                self.grid[road_row][road_col + 1].get_road().set_connect(self.grid[road_row][road_col].get_road(), 0)

        # BL connection
        if road_row < self.nums_grid_y - 1:
            if self.grid[road_row + 1][road_col].get_road():
                self.grid[road_row + 1][road_col].get_road().set_connect(self.grid[road_row][road_col].get_road(), 1)

    def get_grid(self): return self.grid

    def building_add(self, row, col, selected_type):

        if not self.game_controller.has_enough_denier(selected_type):
            return

        building = None
        match selected_type:
            case BuildingTypes.SMALL_TENT:
                building = SmallTent(row, col)
            case BuildingTypes.PREFECTURE:
                building = Prefecture(row, col)
            case BuildingTypes.WELL:
                building = Well(row, col)

        if sum(building.get_building_size()) > 2:
            (x_building, y_building) = building.get_building_size()
            #check if all case are buildable
            try:
                for x in range(col,col+x_building, 1):
                    for y in range(row,row-y_building, -1):
                        if not self.grid[y][x].is_buildable():
                            print("Building can't be construct")
                            return
            except IndexError:
                #We are out of the index of the grid
                return

            # Put building in each case
            for x in range(col,col+x_building,1):
                for y in range(row,row-y_building,-1):
                    if x != col or y != row:
                        self.grid[y][x].set_building(building, False)

        #Show first case
        self.grid[row][col].set_building(building, True)
        self.game_controller.new_building(building)

    def load_map(self, name="default"):
        img = Image.open("maps/small-default.png")

        table = []

        for x in range(img.size[0]):
            table.append([])
            for y in range(img.size[1]):
                r, g, b, a = img.getpixel((y, x))

                tile = Tile(row=x, col=y)

                match (r, g, b):
                    case (255, 242, 0):
                        tile.set_type(TileTypes.WHEAT)
                    case (12, 102, 36):
                        tile.set_building(SmallTree(x, y))
                    case (0, 162, 232):
                        tile.set_type(TileTypes.WATER)
                    case (161, 161, 161):
                        tile.set_building(Rock(x, y))

                table[x].append(tile)

        return table