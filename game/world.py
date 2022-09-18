import pygame as pg
from .setting import *
class World:
    def __init__(self, nums_grid_x, nums_grid_y, height, width):
        self.nums_grid_x = nums_grid_x
        self.nums_grid_y = nums_grid_y
        self.length = height
        self.width = width

    def create_world(self):
        world = []
        for row in range(self.nums_grid_y):
            world.append([])
            for col in range(self.nums_grid_x):
                cartesian_coordination = self.cartesian_coordination(row, col)
                world[row].append(cartesian_coordination)    
        return world
    
    def cartesian_coordination(self, row, col):
        cartesian_coordination = (col*TILE_SIZE, row*TILE_SIZE) # -> (x, y) en pixel
        return cartesian_coordination

    
