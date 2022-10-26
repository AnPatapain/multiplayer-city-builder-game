import pygame as pg
import os
from perlin_noise import PerlinNoise
import random as rd

from .setting import *
import game.utils as utils


class World:

    def __init__(self, nums_grid_x, nums_grid_y, width, height, panel):
        self.nums_grid_x = nums_grid_x
        self.nums_grid_y = nums_grid_y
        self.width = width
        self.height = height
        
        self.noise_scale = nums_grid_x/2
        self.graphics = self.load_images()
        self.default_surface = pg.Surface((nums_grid_x * TILE_SIZE * 2, nums_grid_y * TILE_SIZE + 2 * TILE_SIZE))
        self.grid = self.grid()

        #For building feature
        self.panel = panel
        self.temp_tile = None
        self.start_point = None
        self.temp_end_point = None
        self.end_point = None

        self.in_build_action = False

    def mouse_pos_to_grid(self, mouse_pos, map_pos):
        '''
        Convert the process that transform a mouse_pos to row and col in grid

        convert this process: (col, row) -> convert_to_iso -> offset (1/2 default_surface.width, 0) -> offset (map_pos[0], map_pos[1])

        Arguments: mouse_position: tuple, map_position: tuple

        Return: (col, row) of mouse_position in the grid
        '''

        iso_x = mouse_pos[0] - map_pos[0] - self.default_surface.get_width()/2
        iso_y = mouse_pos[1] - map_pos[1]

        # transform to cart (inverse of cart_to_iso)
        cart_x = (iso_x + 2*iso_y)/2
        cart_y = (2*iso_y - iso_x)/2

        # transform to grid coordinates
        grid_col = int(cart_x // TILE_SIZE)
        grid_row = int(cart_y // TILE_SIZE)
        return (grid_col, grid_row)

    
    def event_handler(self, event, map_pos):

        mouse_pos = pg.mouse.get_pos()
        mouse_grid_pos = self.mouse_pos_to_grid(mouse_pos, map_pos)

        if self.in_map(mouse_grid_pos):
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.start_point = mouse_grid_pos
                    self.in_build_action = True
                      

            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    self.in_build_action = False
                    self.end_point = mouse_grid_pos
                    
                
            elif event.type == pg.MOUSEMOTION:
                self.temp_end_point = mouse_grid_pos
                

    
    def update(self, map_pos):
        '''
        Get mouse_pos -> convert to (col, row) in grid using mouse_pos_to_grid function
        
        if there is selected_tile from panel:
            store name, image of selected_tile and mouse_grid_pos in self.temp_tile so we can draw it in world.draw()

            if left_click:
                bind the texture of the selected_tile at grid[row][col]
                set isBuildable at grid[row][col] False
            
            if right_click:
                set selected_tile in panel False    
        '''
        mouse_pos = pg.mouse.get_pos()
        mouse_grid_pos = self.mouse_pos_to_grid(mouse_pos, map_pos)
        mouse_action = pg.mouse.get_pressed()


        selected_tile = self.panel.get_selected_tile()
        self.temp_tile = None

        if selected_tile != None:
            if self.in_map(mouse_grid_pos):
                self.temp_tile = {
                    'name': selected_tile["name"],
                    'isometric_coor': self.grid[mouse_grid_pos[1]][mouse_grid_pos[0]]["isometric_coor"],
                    'render_img_coor': self.grid[mouse_grid_pos[1]][mouse_grid_pos[0]]["render_img_coor"],
                    'isBuildable': self.grid[mouse_grid_pos[1]][mouse_grid_pos[0]]["isBuildable"]
                }

            if self.in_build_action == False and self.start_point != None and self.end_point != None:

                if self.in_map(self.start_point) and self.in_map(self.end_point):
                    for row in utils.MyRange(self.start_point[1], self.end_point[1]):
                        for col in utils.MyRange(self.start_point[0], self.end_point[0]):

                            if self.grid[row][col]['isBuildable']:
                                self.grid[row][col]["texture"] = self.temp_tile["name"]
                                self.grid[row][col]["isBuildable"] = False

                if mouse_action[2]:
                    self.panel.set_selected_tile(None)

                # if mouse_action[0] and self.temp_tile['isBuildable']:
                #     self.grid[mouse_grid_pos[1]][mouse_grid_pos[0]]["texture"] = self.temp_tile["name"]
                #     self.grid[mouse_grid_pos[1]][mouse_grid_pos[0]]["isBuildable"] = False

                # if self.in_build_action == False:
                #     pass

                # elif mouse_action[2]:
                #     self.panel.set_selected_tile(None)


    def draw(self, screen, map_pos):   
        screen.blit(self.default_surface, map_pos)

        for row in range(self.nums_grid_y):
            for col in range(self.nums_grid_x):
                (x, y) = self.grid[row][col]['render_img_coor']
                # cell is placed at 1/2 default_surface.get_width() and be offseted by the position of the default_surface
                (x_offset, y_offset) = ( x + self.default_surface.get_width()/2 + map_pos[0], 
                                         y + map_pos[1] )

                texture = self.grid[row][col]['texture']
                texture_image = self.graphics['upscale_2x'][texture]

                if texture != 'block':
                    screen.blit(texture_image, (x_offset, y_offset -  texture_image.get_height() + TILE_SIZE))
        
        if self.temp_tile is not None and self.in_build_action == False:
            isometric_coor = self.temp_tile['isometric_coor']
            isometric_coor_offset = [(x+map_pos[0]+self.default_surface.get_width()/2, y + map_pos[1]) for x, y in isometric_coor]

            (x, y) = self.temp_tile['render_img_coor']
            (x_offset, y_offset) = ( x + self.default_surface.get_width()/2 + map_pos[0], 
                                     y + map_pos[1] )

            screen.blit(self.graphics['upscale_2x'][self.temp_tile['name']], 
                       (x_offset, y_offset -  self.graphics['upscale_2x'][self.temp_tile['name']].get_height() + TILE_SIZE))

            if self.temp_tile['isBuildable']:
                pg.draw.polygon(screen, (0, 255, 0), isometric_coor_offset, 4)
            else:
                pg.draw.polygon(screen, (255, 0, 0), isometric_coor_offset, 4)

        
        if self.in_build_action:

            if self.in_map(self.start_point) and self.in_map(self.temp_end_point):
                for row in utils.MyRange(self.start_point[1], self.temp_end_point[1]):
                    for col in utils.MyRange(self.start_point[0], self.temp_end_point[0]):

                        if self.grid[row][col]['isBuildable']:

                            (x, y) = self.grid[row][col]['render_img_coor']

                            (x_offset, y_offset) = ( x + self.default_surface.get_width()/2 + map_pos[0], y + map_pos[1] )
                            temp_house_image = self.graphics['upscale_2x']['temp_house']
                            screen.blit(temp_house_image, (x_offset, y_offset -  temp_house_image.get_height() + TILE_SIZE))
    

    def grid(self):
        grid = []
        for row in range(self.nums_grid_y):

            grid.append([])

            for col in range(self.nums_grid_x):

                iso_tile = self.tile(row, col)
                grid[row].append(iso_tile)

                (x, y) = iso_tile['render_img_coor']
                offset_render = (x + self.default_surface.get_width()/2, y)
                
                self.default_surface.blit(self.graphics['upscale_2x']['block'], offset_render)

        return grid


    def tile(self, row, col):

        def graphic_generator():

            normal_random = rd.randint(1, 100)

            noise = PerlinNoise(octaves=1, seed=777)

            perlin_random = 100 * noise([col/self.noise_scale, row/self.noise_scale])

            # perlin_distribution(perlin_random)
            graphic_ = 'block'
            if (perlin_random >= 20) or perlin_random <= -30 :
                graphic_ = 'tree'
            else:
                if normal_random < 4:
                    graphic_ = 'rock'
                if normal_random < 2:
                    graphic_ = 'tree'
            return graphic_

        graphic = graphic_generator()
        
        cartesian_coor = [
            (col*TILE_SIZE, row*TILE_SIZE),
            (col*TILE_SIZE + TILE_SIZE, row*TILE_SIZE),
            (col*TILE_SIZE + TILE_SIZE, row*TILE_SIZE + TILE_SIZE),
            (col*TILE_SIZE, row*TILE_SIZE + TILE_SIZE)
        ]

        isometric_coor = [self.convert_cart_to_iso(x, y) for x, y in cartesian_coor]

        render_img_coor = (
            min([x for x, y in isometric_coor]), 
            min([y for x, y in isometric_coor])
        )

        return {
            'cartesian_coor': cartesian_coor,
            'isometric_coor': isometric_coor,
            'render_img_coor': render_img_coor,
            'texture': graphic,
            'isBuildable': True if graphic == "block" else False
        }


    def convert_cart_to_iso(self, x, y): return ( x - y, (x + y)/2 )


    def load_images(self):

        path = 'assets/C3_sprites/C3'

        return {
            'origin': {
                'block': pg.image.load(os.path.join(path, 'Land1a_00069.png')).convert_alpha(),
                'tree': pg.image.load(os.path.join(path, 'Land1a_00041.png')).convert_alpha(),
                'rock': pg.image.load(os.path.join(path, 'Land1a_00290.png')).convert_alpha()
            },

            'upscale_2x': {
                'block': self.scale_image_2x( pg.image.load( os.path.join(path, 'Land1a_00069.png') ) ).convert_alpha() ,
                'tree': self.scale_image_2x( pg.image.load( os.path.join(path, 'Land1a_00041.png') ) ).convert_alpha(),
                'rock': self.scale_image_2x( pg.image.load( os.path.join(path, 'Land1a_00290.png') ) ).convert_alpha(),
                'temp_house': self.scale_image_2x(pg.image.load( os.path.join(path, 'Housng1a_00045.png') )).convert_alpha()
            }
        }


    def scale_image_2x(self, image):
        return pg.transform.scale2x(image)


    def in_map(self, grid_pos):
        mouse_on_panel = False
        in_map_limit = (0 <= grid_pos[0] < self.nums_grid_x) and (0 <= grid_pos[1] < self.nums_grid_y)
        for rect in self.panel.get_panel_rects():
            if rect.collidepoint(pg.mouse.get_pos()):
                mouse_on_panel = True
        return True if (in_map_limit and not mouse_on_panel) else False

    
