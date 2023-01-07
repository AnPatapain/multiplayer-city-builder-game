import random
from typing import Optional

import pygame as pg
from PIL import Image

import game.utils as utils
from buildable.buildableCost import buildable_cost
from buildable.final.buildable.rock import Rock
from buildable.final.buildable.tree import SmallTree
from class_types.buildind_types import BuildingTypes
from class_types.orientation_types import OrientationTypes
from class_types.road_types import RoadTypes
from class_types.tile_types import TileTypes
from events.event_manager import EventManager
from game.game_controller import GameController
from game.map_controller import MapController
from game.setting import *
from game.textures import Textures
from map_element.tile import Tile

from game.builder import Builder

class World:

    def __init__(self, nums_grid_x, nums_grid_y, width, height, panel):
        self.game_controller = GameController.get_instance()
        self.nums_grid_x = nums_grid_x
        self.nums_grid_y = nums_grid_y
        self.width = width
        self.height = height

        self.builder = Builder(nums_grid_x, nums_grid_y)

        self.default_surface = pg.Surface((DEFAULT_SURFACE_WIDTH, DEFAULT_SURFACE_HEIGHT)).convert()
        self.load_map()
        self.grid = self.game_controller.get_map()


        '''
        create map only once by bliting texture directly on default surface not on screen and then we can blit default surface on screen 
        '''
        self.create_static_map()

        # For building feature
        self.panel = panel

        #shortcup
        EventManager.register_key_listener(pg.K_h,lambda : self.panel.set_selected_tile(BuildingTypes.VACANT_HOUSE))
        EventManager.register_key_listener(pg.K_d,lambda : self.panel.set_selected_tile(BuildingTypes.PELLE))
        EventManager.register_key_listener(pg.K_p,lambda : self.panel.set_selected_tile(BuildingTypes.PREFECTURE))
        EventManager.register_key_listener(pg.K_r,lambda : self.panel.set_selected_tile(RoadTypes.TL_TO_BR))
        EventManager.register_key_listener(pg.K_w,lambda : self.panel.set_selected_tile(BuildingTypes.WELL))
        EventManager.register_key_listener(pg.K_g, lambda : self.panel.set_selected_tile(BuildingTypes.GRANARY))
        EventManager.register_key_listener(pg.K_f, lambda : self.panel.set_selected_tile(BuildingTypes.WHEAT_FARM))
        EventManager.register_key_listener(pg.K_m, lambda : self.panel.set_selected_tile(BuildingTypes.MARKET))

    def mouse_pos_to_grid(self, mouse_pos):
        """
        DESCRIPTION: Convert position of mouse to row and col on grid. ex: convert (192.15, 30.14) to (row: 40, col: 10)
        To do that we reverse this process: (col, row) -> convert_to_iso -> offset (1/2 default_surface.width, 0) -> offset (map_pos[0], map_pos[1])

        Params: mouse_position: tuple, map_position: tuple

        Return: (col, row) of mouse_position in the grid
        """

        map_pos = MapController.get_map_pos()
        # self.default_surface c'est notre image de fond pour le terrain
        iso_x = mouse_pos[0] - map_pos[0] - self.default_surface.get_width() / 2
        iso_y = mouse_pos[1] - map_pos[1]

        # transform to cart (inverse of cart_to_iso)
        cart_x = (iso_x + 2 * iso_y) / 2
        cart_y = (2 * iso_y - iso_x) / 2

        # transform to grid coordinates
        grid_col = int(cart_x // TILE_SIZE)
        grid_row = int(cart_y // TILE_SIZE)
        return grid_col, grid_row

    def event_handler(self, event):

        """
        DESCRIPTION: Handling the events that be gotten from event queue in module event_manager.py

        Params: event retrieved from pg.event.get() in event_manager.py, map_position in map_controller.py

        Return: None
        """

        mouse_pos = pg.mouse.get_pos()
        mouse_grid_pos = self.mouse_pos_to_grid(mouse_pos)

        if self.in_map(mouse_grid_pos):
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1 and self.panel.has_selected_tile():
                    self.builder.set_start_point(mouse_grid_pos)
                    self.builder.set_end_point(mouse_grid_pos)
                    self.builder.set_in_build_action(True)

            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 1 and self.panel.has_selected_tile():
                    self.builder.set_in_build_action(False)
                    self.builder.set_end_point(mouse_grid_pos)

            elif event.type == pg.MOUSEMOTION:
                self.builder.set_end_point(mouse_grid_pos)

    def update(self):
        """
        DESCRIPTION: updating the state of the world. For now it updates temp_tile, texture of the world
        
        Return: None
        """
        mouse_pos = pg.mouse.get_pos()
        mouse_grid_pos = self.mouse_pos_to_grid(mouse_pos)
        mouse_action = pg.mouse.get_pressed()

        selected_tile = self.panel.get_selected_tile()
        self.builder.set_temp_tile_info(None)

        if selected_tile:
            grid = self.game_controller.get_map()
            if self.in_map(mouse_grid_pos):
                tile = grid[mouse_grid_pos[1]][mouse_grid_pos[0]]

                self.builder.set_temp_tile_info({
                    'name': selected_tile,
                    'isometric_coor': tile.get_isometric_coord(),
                    'render_img_coor': tile.get_render_coord(),
                    'isBuildable': tile.is_buildable(),
                    'isDestroyable': tile.is_destroyable()
                })

            # Build from start point to end point
            if not self.builder.get_in_build_action() and self.builder.get_start_point() and self.builder.get_end_point():
                if self.in_map(self.builder.get_start_point()) and self.in_map(self.builder.get_end_point()):
                    start_point = self.builder.get_start_point()
                    end_point = self.builder.get_end_point()
                    self.builder.build_from_start_to_end(selected_tile, start_point, end_point)

                    self.builder.set_start_point(None)  # update start point to default after building
                    self.builder.set_end_point(None)  # update start point to default after building

            if mouse_action[2]:
                self.panel.set_selected_tile(None)
                self.builder.set_start_point(None)
                self.builder.set_end_point(None)
                self.builder.set_in_build_action(False)

    def draw(self, screen):
        map_pos = MapController.get_map_pos()
        screen.blit(self.default_surface, map_pos)

        for row in self.game_controller.get_map():
            for tile in row:
                (x, y) = tile.get_render_coord()
                (x_offset, y_offset) = (x + self.default_surface.get_width() / 2 + map_pos[0], y + map_pos[1])

                if tile.get_road() or tile.get_building():
                    screen.blit(tile.get_texture(), (x_offset, y_offset - tile.get_texture().get_height() + TILE_SIZE))

                base_x_offset = x_offset
                base_y_offset = y_offset
                for walker in tile.walkers:
                    x_offset = x_offset + TILE_SIZE/2

                    orient = walker.orientation_from_previous_tile if walker.walk_progression < 0 else walker.orientation_to_next_tile
                    match orient:
                        case OrientationTypes.TOP_RIGHT:
                            x_offset += walker.walk_progression*2
                            y_offset -= walker.walk_progression
                        case OrientationTypes.TOP_LEFT:
                            x_offset -= walker.walk_progression*2
                            y_offset -= walker.walk_progression
                        case OrientationTypes.BOTTOM_LEFT:
                            x_offset -= walker.walk_progression*2
                            y_offset += walker.walk_progression
                        case OrientationTypes.BOTTOM_RIGHT:
                            x_offset += walker.walk_progression*2
                            y_offset += walker.walk_progression

                    screen.blit(walker.get_texture(), (x_offset, y_offset))
                    x_offset = base_x_offset
                    y_offset = base_y_offset

        if self.builder.get_temp_tile_info() and not self.builder.get_in_build_action():
            isometric_coor = self.builder.get_temp_tile_info()['isometric_coor']
            isometric_coor_offset = [(x + map_pos[0] + self.default_surface.get_width() / 2, y + map_pos[1]) for x, y in
                                     isometric_coor]

            (x, y) = self.builder.get_temp_tile_info()['render_img_coor']
            (x_offset, y_offset) = (x + self.default_surface.get_width() / 2 + map_pos[0],
                                    y + map_pos[1])

            texture = Textures.get_texture(self.builder.get_temp_tile_info()['name'])
            screen.blit(texture, (x_offset, y_offset - texture.get_height() + TILE_SIZE))

            if self.builder.get_temp_tile_info()['isBuildable']:
                pg.draw.polygon(screen, (0, 255, 0), isometric_coor_offset)
            else:
                pg.draw.polygon(screen, (255, 0, 0), isometric_coor_offset)

            if self.panel.selected_tile:
                cost = buildable_cost[self.panel.selected_tile]
                if self.panel.selected_tile == BuildingTypes.PELLE:
                    cost = 0
                utils.draw_text(text=str(cost), pos=isometric_coor_offset[1], screen=screen, size=30, color=pg.Color(255, 255, 0))

        if self.builder.get_in_build_action():

            if self.in_map(self.builder.get_start_point()) and self.in_map(self.builder.get_end_point()):
                grid = self.game_controller.get_map()

                if self.panel.selected_tile == RoadTypes.TL_TO_BR:
                    start = grid[self.builder.get_start_point()[1]][self.builder.get_start_point()[0]]
                    if not start.is_buildable() and not start.get_road():
                        return
                    end = grid[self.builder.get_end_point()[1]][self.builder.get_end_point()[0]]
                    if not end.is_buildable() and not end.get_road():
                        return
                    path = start.find_path_to(end, buildable_or_road=True)

                    if path:
                        to_build_number = 0
                        for tile in path:
                            # Don't display build sign if there is already a road
                            if tile.get_road() or not tile.is_buildable():
                                continue
                            (x, y) = tile.get_render_coord()
                            (x_offset, y_offset) = (x + self.default_surface.get_width() / 2 + map_pos[0], y + map_pos[1])
                            build_sign = Textures.get_texture(BuildingTypes.BUILD_SIGN)
                            screen.blit(build_sign,
                                        (x_offset, y_offset - build_sign.get_height() + TILE_SIZE))
                            to_build_number += 1

                        isometric_coor = self.builder.get_temp_tile_info()['isometric_coor']
                        isometric_coor_offset = [(x + map_pos[0] + self.default_surface.get_width() / 2, y + map_pos[1]) for x, y in
                                                 isometric_coor]
                        utils.draw_text(text=str(to_build_number*4), pos=isometric_coor_offset[1], screen=screen, size=30, color=pg.Color(255, 255, 0))

                    return

                count = 0
                for row in utils.MyRange(self.builder.get_start_point()[1], self.builder.get_end_point()[1]):
                    for col in utils.MyRange(self.builder.get_start_point()[0], self.builder.get_end_point()[0]):

                        (x, y) = grid[row][col].get_render_coord()
                        (x_offset, y_offset) = ( x + self.default_surface.get_width() / 2 + map_pos[0], y + map_pos[1] )

                        if grid[row][col].is_buildable() and self.builder.get_temp_tile_info() and self.builder.get_temp_tile_info()["name"] != BuildingTypes.PELLE:
                            build_sign = Textures.get_texture(BuildingTypes.BUILD_SIGN)
                            count += 1
                            screen.blit(build_sign,
                                        (x_offset, y_offset - build_sign.get_height() + TILE_SIZE))

                        elif grid[row][col].is_destroyable() and self.builder.get_temp_tile_info() and self.builder.get_temp_tile_info()["name"] == BuildingTypes.PELLE:
                            building = grid[row][col].get_delete_texture()
                            count += 1
                            screen.blit(building,
                                        (x_offset, y_offset - building.get_height() + TILE_SIZE))

                isometric_coor = self.builder.get_temp_tile_info()['isometric_coor']
                isometric_coor_offset = [(x + map_pos[0] + self.default_surface.get_width() / 2, y + map_pos[1]) for x, y in
                                                 isometric_coor]
                utils.draw_text(text=str(count*buildable_cost[self.panel.selected_tile]), pos=isometric_coor_offset[1], screen=screen, size=30, color=pg.Color(255, 255, 0))

    def create_static_map(self):
        for row in self.game_controller.get_map():
            for tile in row:
                tile: Tile = tile
                texture_image = Textures.get_texture(tile.type, texture_number=tile.get_random_texture_number())
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

    def load_map(self):
        img = Image.open("maps/map.png")

        rock_list = []
        table: list[list[Tile]] = []
        spawn_point: Optional[Tile] = None
        leave_point: Optional[Tile] = None

        for x in range(img.size[0]):
            table.append([])
            for y in range(img.size[1]):
                r, g, b, a = img.getpixel((y, x))

                tile = Tile(row=x, col=y)

                match (r, g, b):
                    case (255, 242, 0):
                        tile.set_type(TileTypes.WHEAT)
                        tile.set_random_texture_number(random.randint(0, 3))
                    case (12, 102, 36):
                        tile.set_building(SmallTree(x, y))
                        tile.set_random_texture_number(random.randint(7, 30))
                    case (0, 162, 232):
                        tile.set_type(TileTypes.WATER)
                        tile.set_random_texture_number(random.randint(0, 7))
                        self.riviere(x, y, img, tile)
                    case (161, 161, 161):
                        tile.set_building(Rock(x, y))
                        tile.set_random_texture_number(random.randint(0, 7))
                        self.random_rock(x, y, img, tile, rock_list)
                    case (237, 28, 35):
                        pass  # Red color, flag spawn
                    case (111, 49, 152):
                        pass  # Purple color, flag leave
                    case (153, 0, 48):
                        spawn_point = tile
                        pass  # Brown/Red, road spawn
                    case (181, 165, 213):
                        leave_point = tile
                        pass  # Purple/Brown, road leave
                    case _:
                        tile.set_random_texture_number(random.randint(0, 20))

                table[x].append(tile)

        self.game_controller.set_map(table)
        self.game_controller.spawn_point = spawn_point
        self.game_controller.leave_point = leave_point

        # The map need to exist to add roads
        for x in range(img.size[0]):
            for y in range(img.size[1]):
                r, g, b, a = img.getpixel((y, x))
                match (r, g, b):
                    case (156, 90, 60):
                        self.builder.road_add(x, y) # Brown color, road
                    case (153, 0, 48):
                        self.builder.road_add(x, y)
                    case (181, 165, 213):
                        self.builder.road_add(x, y)

        self.riviere_angle()
        self.wheat()
        #self.rochers()

    def riviere(self, x, y, img, tile):
        if 0 <= y <= 39 and 0 <= x <= 39:
            r_d, r_b, r_g, r_h = 0, 0, 0, 0
            if x != 0 and y != 0 and x != 39 and y != 39:
                r_d, g_d, b_d, a_d = img.getpixel((y, x - 1))
                r_g, g_g, b_g, a_g = img.getpixel((y, x + 1))
                r_h, g_h, b_h, a_h = img.getpixel((y - 1, x))
                r_b, g_b, b_b, a_b = img.getpixel((y + 1, x))
            else:
                if x == 0 and y != 0:
                    r_d = 0
                    r_g, g_g, b_g, a_g = img.getpixel((y, x + 1))
                    r_h, g_h, b_h, a_h = img.getpixel((y - 1, x))
                    r_b, g_b, b_b, a_b = img.getpixel((y + 1, x))
                if y == 0 and x != 0:
                    r_d, g_d, b_d, a_d = img.getpixel((y, x - 1))
                    r_g, g_g, b_g, a_g = img.getpixel((y, x + 1))
                    r_b, g_b, b_b, a_b = img.getpixel((y + 1, x))
                    r_h = 0
                if x == 39 and y != 39:
                    r_d, g_d, b_d, a_d = img.getpixel((y, x - 1))
                    r_h, g_h, b_h, a_h = img.getpixel((y - 1, x))
                    r_b, g_b, b_b, a_b = img.getpixel((y + 1, x))
                    r_g = 0
                if y == 39 and x != 39:
                    r_d, g_d, b_d, a_d = img.getpixel((y, x - 1))
                    r_g, g_g, b_g, a_g = img.getpixel((y, x + 1))
                    r_h, g_h, b_h, a_h = img.getpixel((y - 1, x))
                    r_b = 0

            if r_d != 0:
                tile.set_random_texture_number(10)
                if r_h != 0 and r_b == 0:
                    tile.set_random_texture_number(11)
                elif r_b != 0 and r_h == 0:
                    tile.set_random_texture_number(12)
                elif r_b != 0 and r_h != 0:
                    tile.set_random_texture_number(13)

            if r_h != 0:
                tile.set_random_texture_number(14)
                if r_d != 0 and r_g == 0:
                    tile.set_random_texture_number(11)
                elif r_g != 0 and r_d == 0:
                    tile.set_random_texture_number(15)
                elif r_d != 0 and r_g != 0:
                    tile.set_random_texture_number(16)

            if r_g != 0:
                tile.set_random_texture_number(17)
                if r_h != 0 and r_b == 0:
                    tile.set_random_texture_number(18)
                elif r_b != 0 and r_h == 0:
                    tile.set_random_texture_number(19)
                elif r_b != 0 and r_h != 0:
                    tile.set_random_texture_number(20)

            if r_b != 0:
                tile.set_random_texture_number(21)
                if r_d != 0 and r_g == 0:
                    tile.set_random_texture_number(22)
                elif r_g != 0 and r_d == 0:
                    tile.set_random_texture_number(23)
                elif r_d != 0 and r_g != 0:
                    tile.set_random_texture_number(24)



    def riviere_angle(self):
        grid = self.game_controller.get_map()
        for x in range(0, 40):
            for y in range(0, 39):
                tile = grid[x][y]

                if tile.get_type() == TileTypes.WATER:
                    tile_g = grid[x][y-1]
                    tile_d = grid[x][y+1]
                    tile_h = grid[x-1][y]
                    tile_b = grid[x+1][y]



                    if tile_b.get_type() == TileTypes.WATER and tile_g.get_type() == TileTypes.WATER and tile_b.get_random_texture_number() in range(10, 24) and tile_g.get_random_texture_number() in range(10, 24):
                        if grid[x+1][y-1].get_type() != TileTypes.WATER:
                            tile.set_random_texture_number(70)
                    if tile_b.get_type() == TileTypes.WATER and tile_d.get_type() == TileTypes.WATER and tile_b.get_random_texture_number() in range(10, 24) and tile_d.get_random_texture_number() in range(10, 24):
                        tile.set_random_texture_number(71)
                    if tile_g.get_type() == TileTypes.WATER and tile_h.get_type() == TileTypes.WATER and tile_h.get_random_texture_number() in range(10, 24) and tile_g.get_random_texture_number() in range(10, 24):
                        tile.set_random_texture_number(72)
                    if tile_h.get_type() == TileTypes.WATER and tile_d.get_type() == TileTypes.WATER and tile_h.get_random_texture_number() in range(10, 24) and tile_d.get_random_texture_number() in range(10, 24):
                        if tile_b.get_type() == TileTypes.WATER:
                            tile.set_random_texture_number(73)

    def wheat(self):
        grid = self.game_controller.get_map()
        for x in range(1, 38):
            for y in range(1, 38):
                tile = grid[x][y]

                if tile.get_type() == TileTypes.WHEAT:
                    tile_g = grid[x][y - 1]
                    tile_d = grid[x][y + 1]
                    tile_h = grid[x - 1][y]
                    tile_b = grid[x + 1][y]

                    if tile_b.get_type() != TileTypes.WHEAT and tile_g.get_type() != TileTypes.WHEAT:
                        tile.set_random_texture_number(10)
                    if tile_b.get_type() != TileTypes.WHEAT and tile_d.get_type() != TileTypes.WHEAT:
                        tile.set_random_texture_number(11)
                    if tile_g.get_type() != TileTypes.WHEAT and tile_h.get_type() != TileTypes.WHEAT:
                        tile.set_random_texture_number(12)
                    if tile_h.get_type() != TileTypes.WHEAT and tile_d.get_type() != TileTypes.WHEAT:
                        tile.set_random_texture_number(13)

        for x in range(1, 38):
            for y in range(1, 38):
                tile = grid[x][y]

                if tile.get_type() == TileTypes.WHEAT:

                    adj = tile.get_adjacente_tiles()
                    for i in range(len(adj)):
                        if adj[i].get_random_texture_number() in range(10,13):
                            tile.set_random_texture_number(random.randint(20, 23))


    def random_rock(self, x, y, img, tile, rock_list):
        if 0 <= y <= 39 and 0 <= x <= 39:

            r_g, g_d, b_d, a_d = img.getpixel((y, x - 1))
            r_h, g_b, b_b, a_b = img.getpixel((y - 1, x))
            r_hg, g_bd, b_bd, a_bd = img.getpixel((y - 1, x - 1))

            if (r_g, r_h, r_hg) == (161, 161, 161) and (y, x - 1) not in rock_list and (y - 1, x) not in rock_list and (y - 1, x - 1) not in rock_list:
                tile.set_random_texture_number(random.randint(20, 23))
                rock_list.append((y, x-1))
                rock_list.append((y-1, x))
                rock_list.append((y-1, x-1))




