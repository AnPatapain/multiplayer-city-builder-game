import pygame as pg
import os
from perlin_noise import PerlinNoise
from .setting import *
import random as rd


class World:

    def __init__(self, nums_grid_x, nums_grid_y, width, height):

        self.nums_grid_x = nums_grid_x
        self.nums_grid_y = nums_grid_y
        self.width = width
        self.height = height
        
        self.noise_scale = nums_grid_x/2
        self.graphics = self.load_images()
        self.default_surface = pg.Surface((nums_grid_x * TILE_SIZE * 2, nums_grid_y * TILE_SIZE + 2 * TILE_SIZE))
        self.isometric_map = self.isometric_map()


    def draw(self, screen, map_position):
        
        screen.blit(self.default_surface, map_position)

        for row in range(self.nums_grid_y):
            for col in range(self.nums_grid_x):
                
                # Render graphic
                (x, y) = self.isometric_map[row][col]['render_img_coor']

                # cell places at 1/2 default_surface.get_width() and default_surface move around on the screen
                (x_offset, y_offset) = ( x + self.default_surface.get_width()/2 + map_position[0], 
                                         y + map_position[1] )

                graphic_object_name = self.isometric_map[row][col]['texture']

                graphic_object_img = self.graphics['upscale_2x'][graphic_object_name]

                graphic_render = (x_offset, y_offset -  graphic_object_img.get_height() + TILE_SIZE)
                

                if graphic_object_name != 'block':

                    screen.blit(graphic_object_img, graphic_render)

                    self.isometric_map[row][col]['isBuildable'] = False


    # def cartesian_map(self):

    #     world = []
    #     for row in range(self.nums_grid_y):
    #         world.append([])
    #         for col in range(self.nums_grid_x):
    #             cartesian_cell = self.cartesian_cell(row, col)
    #             world[row].append(cartesian_cell)    
    #     return world
    

    def isometric_map(self):

        map = []
        for row in range(self.nums_grid_y):

            map.append([])

            for col in range(self.nums_grid_x):

                iso_tile = self.tile(row, col)
                map[row].append(iso_tile)

                (x, y) = iso_tile['render_img_coor']
                offset_render = (x + self.default_surface.get_width()/2, y)
                
                self.default_surface.blit(self.graphics['upscale_2x']['block'], offset_render)

        return map


    def tile(self, row, col):

        def graphic_generator():

            normal_random = rd.randint(1, 100)

            noise = PerlinNoise(octaves=1, seed=777)

            perlin_random = 100 * noise([col/self.noise_scale, row/self.noise_scale])

            # perlin_distribution(perlin_random)
            
            graphic = 'block'
            if (perlin_random >= 20) or perlin_random <= -30 :
                graphic = 'tree'
            else:
                if normal_random < 4:
                    graphic = 'rock'
                if normal_random < 2:
                    graphic = 'tree'
            return graphic
        
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
            'texture': graphic_generator(),
            'isBuildable': True
        }


    def convert_cart_to_iso(self, x, y): return ( x - y, (x + y)/2 )


    def load_images(self):

        path = 'assets/graphics'
        upscale_path = 'assets/upscaled_graphics'
        return {
            'origin': {
                'block': pg.image.load(os.path.join(path, 'Land1a_00069.png')).convert_alpha(),
                'tree': pg.image.load(os.path.join(path, 'Land1a_00041.png')).convert_alpha(),
                'rock': pg.image.load(os.path.join(path, 'Land1a_00290.png')).convert_alpha()
            },
            'upscale_4x': {
                'block': pg.image.load(os.path.join(upscale_path, 'Land1a_00069_upscaled.png')).convert_alpha(),
                'tree': pg.image.load(os.path.join(upscale_path, 'Land1a_00041_upscaled.png')).convert_alpha(),
                'rock': pg.image.load(os.path.join(upscale_path, 'Land1a_00290_upscaled.png')).convert_alpha(),
                'mountain': pg.image.load(os.path.join(upscale_path, 'land3a_00074_upscaled.png')).convert_alpha()
            },
            'upscale_2x': {
                'block': self.scale_image_2x( pg.image.load( os.path.join(path, 'Land1a_00069.png') ) ).convert_alpha() ,
                'tree': self.scale_image_2x( pg.image.load( os.path.join(path, 'Land1a_00041.png') ) ).convert_alpha(),
                'rock': self.scale_image_2x( pg.image.load( os.path.join(path, 'Land1a_00290.png') ) ).convert_alpha()
            }
        }


    def scale_image_2x(self, image):
        
        # built-in function of pygame for scaling image to 2x 
        return pg.transform.scale2x(image)

    
