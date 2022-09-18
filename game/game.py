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
        world = self.world.create_world()

        for row in range(self.world.nums_grid_y):
            for col in range(self.world.nums_grid_x):
                # Retrive each rect coordination (by pixel) from world grid
                # Draw each rect from these coordination
                rect = pg.Rect(world[row][col][0][0], world[row][col][0][1] , TILE_SIZE, TILE_SIZE)
                pg.draw.rect(self.screen, (255, 255, 255), rect, 1)

        pg.display.flip()


    def update(self):
        pass
