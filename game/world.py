import pygame as pg
import os
from .setting import *


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

        return {
            'isometric_cell': isometric_cell,
            'render_img_coor': render_img_coor
        }
        # return isometric_cell

    def load_images(self):
        path = 'assets/graphics'
        return {
            'block': pg.image.load(os.path.join(path, 'Land2a_00040.png'))
        }

    
