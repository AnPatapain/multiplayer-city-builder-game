import pygame as pg
import sys
from .world import World
from .utils import draw_text
from .map_controller import Map_controller
from .panel import Panel
from .setting import *


class Game:

    def __init__(self, screen, clock):

        self.screen = screen
        self.clock = clock
        self.width, self.height = self.screen.get_size()

        # map_controller update position of surface that the map blited on according to mouse position or key event
        self.map_controller = Map_controller(self.width, self.height)

        # panel has two sub_panel: ressource_panel for displaying Dn, Populations, etc and building_panel
        # for displaying available building in game
        self.panel = Panel(self.width, self.height)

        # World contains populations or graphical objects like buildings, trees, grass
        self.world = World(NUMS_GRID_X, NUMS_GRID_Y, self.width, self.height, self.panel)

        


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
                self.map_controller.event_handler(event)

            self.world.event_handler(event, self.map_controller.get_map_pos())
                
                

    def draw(self):
        self.screen.fill((0, 0, 0))

        self.world.draw(self.screen, self.map_controller.get_map_pos())

        self.panel.draw(self.screen)

        draw_text('fps={}'.format(round(self.clock.get_fps())), self.screen, (self.width - 200, 20), size=42)
                
        pg.display.flip()


    def update(self):
        self.map_controller.update_map_pos()
        self.panel.update()
        self.world.update(self.map_controller.get_map_pos())
