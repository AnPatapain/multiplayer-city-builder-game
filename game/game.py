import pygame as pg
import sys
from .world import World
from .setting import *


class Game:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.width, self.height = self.screen.get_size()
        self.world = World(NUMS_GRID_X, NUMS_GRID_Y, self.width, self.height)

    # Game Loop
    def run(self):
        self.playing = True
        
        while self.playing:
            self.clock.tick(60)
            self.draw()
            self.event_handler()
            self.update()
        

    def event_handler(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
                
                # For scrolling map
                if event.key == pg.K_DOWN:
                    self.world.map_position[1] = self.world.map_position[1] - 200
                if event.key == pg.K_UP:
                    self.world.map_position[1] = self.world.map_position[1] + 200
                if event.key == pg.K_LEFT:
                    self.world.map_position[0] = self.world.map_position[0] + 200
                if event.key == pg.K_RIGHT:
                    self.world.map_position[0] = self.world.map_position[0] - 200

    def draw(self):
        self.screen.fill((0, 0, 0))
        isometric_map = self.world.isometric_map
        self.screen.blit(self.world.default_surface, self.world.map_position)
        for row in range(self.world.nums_grid_y):
            for col in range(self.world.nums_grid_x):

                # Render graphic
                (x, y) = isometric_map[row][col]['render_img_coor']
                (x, y) = (x + self.world.default_surface_width/2, y + self.world.default_surface_height/4)

                graphic_name = isometric_map[row][col]['graphic']
                graphic_img = self.world.graphics['upscale_4x'][graphic_name]
                graphic_render = (x, y -  graphic_img.get_height() + TILE_SIZE)
                
                if graphic_name != 'block':
                    self.world.default_surface.blit(graphic_img, graphic_render)
                

                # Render grid
                # cell_render = isometric_world[row][col]['isometric_cell']
                # cell_render = [(x + self.width/2, y + self.height/4) for x, y in cell_render]
                # pg.draw.polygon(self.screen, (0, 0, 255), cell_render, 1)
                
        pg.display.flip()


    def update(self):
        pass
