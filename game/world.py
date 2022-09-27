import pygame as pg
import os
from .setting import *
import random as rd


class World:
    def __init__(self, nums_grid_x, nums_grid_y, width, height):
        self.nums_grid_x = nums_grid_x
        self.nums_grid_y = nums_grid_y
        self.height = height
        self.width = width

        self.graphics = self.load_images()
        self.default_surface = pg.Surface((width, height))
        self.isometric_world = self.create_isometric_world()

    def create_cartesian_world(self):
        world = []
        for row in range(self.nums_grid_y):
            world.append([])
            for col in range(self.nums_grid_x):
                cartesian_cell = self.cartesian_cell(row, col)
                world[row].append(cartesian_cell)    
        return world
    

    def create_isometric_world(self):
        world = []
        for row in range(self.nums_grid_y):
            world.append([])
            for col in range(self.nums_grid_x):
                cartesian_cell = self.cartesian_cell(row, col)
                isometric_cell = self.isometric_cell(cartesian_cell)
                world[row].append(isometric_cell)

                (x, y) = isometric_cell['render_img_coor']
                offset_render = (x + self.width/2, y + self.height/4)
                self.default_surface.blit(self.graphics['upscale_4x']['block'], offset_render)

        return world


    # return a cell that contain the cartesian coordination of all vertices
    def cartesian_cell(self, row, col):
        cell = [
            (col*TILE_SIZE, row*TILE_SIZE),
            (col*TILE_SIZE + TILE_SIZE, row*TILE_SIZE),
            (col*TILE_SIZE + TILE_SIZE, row*TILE_SIZE + TILE_SIZE),
            (col*TILE_SIZE, row*TILE_SIZE + TILE_SIZE)
        ]
        return cell
    
    # Convert the coordinations of 4 vertices of square in cartesian basis to isometric basis
    def isometric_cell(self, cartesian_cell):
        convert_function = lambda x, y: (x -y, x/2 + y/2) # for more info about this function search gg with keyword: cartesian to isometric map
        isometric_cell = [convert_function(x, y) for x, y in cartesian_cell]
        
        render_img_coor = (
            min([x for x, y in isometric_cell]), 
            min([y for x, y in isometric_cell])
        )

        def graphic_generator():
            random = rd.randint(1, 100)
            graphic = 'block'
            if random < 10:
                graphic = 'tree'
            elif random >= 10 and random < 20:
                graphic = 'rock'
            return graphic

        return {
            'isometric_cell': isometric_cell,
            'render_img_coor': render_img_coor,
            'graphic': graphic_generator()
        }
        # return isometric_cell

    def load_images(self):
        path = 'assets/graphics'
        upscale_path = 'assets/upscaled_graphics'
        return {
            'origin': {
                'block': pg.image.load(os.path.join(path, 'Land1a_00069.png')),
                'tree': pg.image.load(os.path.join(path, 'Land1a_00041.png')),
                'rock': pg.image.load(os.path.join(path, 'Land1a_00290.png'))
            },
            'upscale_4x': {
                'block': pg.image.load(os.path.join(upscale_path, 'Land1a_00069_upscaled.png')),
                'tree': pg.image.load(os.path.join(upscale_path, 'Land1a_00041_upscaled.png')),
                'rock': pg.image.load(os.path.join(upscale_path, 'Land1a_00290_upscaled.png'))
            }
            
        }

    
