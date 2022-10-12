import pygame as pg
from .button import Button
from .setting import *
import sys
import os


class Menu:
    def __init__(self, screen):

        self.menu_graphics = self.load_menu_graphics()
        self.screen = screen
        self.screen_size = screen.get_size() # -> tuple (width, height)

    def display(self):

        self.display_background_init()
        
        self.display_background_menu()

        # displaying = True

        # start_new_career = Button ( self.menu_graphics['start_new_career'] )
        # load_saved_game = Button (self.menu_graphics['load_saved_game'])
        # options = Button (self.menu_graphics['options'])
        # exit_button = Button ( self.menu_graphics['exit_button'] )
        
        # while displaying:

        #     if start_new_career.clicked():
        #         displaying = False

        #     elif load_saved_game.clicked():
        #         self.load_saved_game_display()

        #     elif options.clicked():
        #         self.options_display()

        #     elif exit_button.clicked():
        #         sys.exit()
        #     pass

        # pass
    
    def display_background_init():
        pass

    def display_background_menu():
        pass

    def load_saved_game_display(self):
        pass

    def options_display(self):
        pass

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