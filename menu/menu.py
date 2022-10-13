from operator import is_
import pygame as pg
from .button import Button
from .setting import *
import sys
import os


class Menu:
    def __init__(self, screen, clock):

        self.screen = screen
        self.clock = clock
        
        self.screen_size = screen.get_size() # -> tuple (width, height)
        self.menu_graphics = self.load_menu_graphics()

        self.start_game = False
        self.is_display_background_init = True
        self.is_display_game_menu = False
        

    def run(self):
        
        while self.start_game == False:
            self.clock.tick(60)
            self.draw()
            self.event_handler()
            self.update()

    def update(self):
        pass


    def event_handler(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if event.type == pg.KEYDOWN:

                if self.is_display_background_init:
                    self.start_game = True

                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
                


    
    def draw(self):

        if self.is_display_background_init :
            self.display_background_init()

        if self.is_display_game_menu:
            self.display_background_menu()

        pg.display.flip()

    
    def display_background_init(self):

        background = pg.transform.scale(self.menu_graphics['background_init'], self.screen_size)
        self.screen.blit(background, (0, 0)) 

    def load_menu_graphics(self):

        path = 'assets/menu_sprites/'       

        return {
            'background_init': pg.image.load(os.path.join(path, 'Background_Init.png')),
            'background_menu': pg.image.load(os.path.join(path, 'Background_Menu.png')),
            'background_start': pg.image.load(os.path.join(path, 'Start.png')),

            'logo': pg.image.load(os.path.join(path, 'Caesar3.png')),
            'start_new_career':  pg.image.load(os.path.join(path, 'start new career.png')),
            'load_saved_game': pg.image.load(os.path.join(path, 'load saved game.png')),
            'options': pg.image.load(os.path.join(path, 'options.png')),
            'exit_button': pg.image.load(os.path.join(path, 'exit.png'))
        }