import pygame as pg
import sys
from .world import World
from .utils import draw_text
from .map_controller import Map_controller
from .setting import *


class Game:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.width, self.height = self.screen.get_size()
        self.world = World(NUMS_GRID_X, NUMS_GRID_Y, self.width, self.height)
        self.map_controller = Map_controller(self.width, self.height)

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
                self.map_controller.key_event_handling(event)
                
                

    def draw(self):
        self.screen.fill((0, 0, 0))

        isometric_map = self.world.isometric_map
        
        self.screen.blit(self.world.default_surface, self.map_controller.map_position)
        for row in range(self.world.nums_grid_y):
            for col in range(self.world.nums_grid_x):
                
                # Render graphic
                (x, y) = isometric_map[row][col]['render_img_coor']
                (x_offset, y_offset) = (x + self.map_controller.map_position[0] + self.world.default_surface.get_width()/2, 
                                        y + self.map_controller.map_position[1])

                graphic_name = isometric_map[row][col]['graphic']
                graphic_img = self.world.graphics['upscale_2x'][graphic_name]
                graphic_render = (x_offset, y_offset -  graphic_img.get_height() + TILE_SIZE)
                
                if graphic_name != 'block':
                    self.screen.blit(graphic_img, graphic_render)

        
        draw_text('fps={}'.format(round(self.clock.get_fps())), self.screen, (10, 10))        
        pg.display.flip()


    def update(self):
        # update map position depending on mouse movement 
        self.map_controller.update_map_position()
