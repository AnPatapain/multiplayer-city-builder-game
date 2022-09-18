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
                cartesian_cell = self.cartesian_cell(row, col)
                world[row].append(cartesian_cell)    
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
    

    
