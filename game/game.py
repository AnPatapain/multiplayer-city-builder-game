from cmath import rect
import pygame as pg
import sys
from .world import World
from .setting import *


class Game:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.width, self.height = self.screen.get_size()
        self.world = World(NUMS_GRID_X, NUMS_GRID_Y, self.height, self.width)


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

    def draw(self):
        self.screen.fill((0, 0, 0))
        cartesian_world = self.world.create_cartesian_world()
        isometric_world = self.world.create_isometric_world()

        for row in range(self.world.nums_grid_y):
            for col in range(self.world.nums_grid_x):
                # Create and Draw each rect from coordinations that be retrieved from world grid

                # cartesian_world[row][col] = [(x + self.width/2, y + self.height/4) for x, y in cartesian_world[row][col]]
                # rect = pg.Rect(cartesian_world[row][col][0][0], cartesian_world[row][col][0][1] , TILE_SIZE, TILE_SIZE)
                # pg.draw.rect(self.screen, (255, 0, 0), rect, 1)

                isometric_world[row][col]['isometric_cell'] = [(x + self.width/2, y + self.height/2) for x, y in isometric_world[row][col]['isometric_cell']]
                pg.draw.polygon(self.screen, (0, 255, 0), isometric_world[row][col]['isometric_cell'], 1)

                # this_Surface.blit(source_Surface, [upper_left_corner_x, upper_left_corner_y])
                (x, y) = isometric_world[row][col]['render_img_coor']
                render_after_offset = (x + self.width/2, y + self.height/4)
                self.screen.blit(self.world.land, render_after_offset)
                
        pg.display.flip()


    def update(self):
        pass
