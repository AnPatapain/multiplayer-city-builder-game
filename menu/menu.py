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
        # self.buttons = [Button(button_name, button_image) for (button_name, button_image) in self.menu_graphics['button'].items()]
        self.buttons = self.load_buttons()

        self.start_game = False
        self.exit = False
        self.is_display_background_init = True
        self.is_display_game_menu = False

    def init(self):
        for i in range(len(self.buttons)):
            original_image = self.buttons[i].get_image()
            scale_image = pg.transform.scale(original_image, (self.screen_size[0]/3, self.screen_size[1]/15))
            self.buttons[i].set_image(scale_image)

            self.buttons[i].set_margin_top(40)
            self.buttons[i].set_position( (self.screen_size[0]/3, 
                                           self.screen_size[1]/5 + i * ( self.buttons[i].get_button_size()[1] + self.buttons[i].get_margin_top() ) ) )


            self.buttons[i].set_rect( self.buttons[i].get_position(), self.buttons[i].get_image().get_size())
                                                                
        

    def run(self):

        self.init()
        
        while self.start_game == False:
            self.clock.tick(60)
            self.draw()
            self.event_handler()
            self.update()


    def update(self):

        mouse_action = pg.mouse.get_pressed()

        if mouse_action[0] and self.is_display_background_init:
            self.is_display_background_init = False
            self.is_display_game_menu = True
        
        elif self.is_display_game_menu:
            for button in self.buttons:

                if button.check_button():
                    
                    if button.get_name() == 'start_new_career':
                        self.start_game = True

                    elif button.get_name() == 'load_saved_game':
                        self.load_saved_game_render()

                    elif button.get_name() == 'options':
                        self.options_render()

                    elif button.get_name() == 'exit_button':
                        sys.exit()


    def event_handler(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if event.type == pg.KEYDOWN:

                if self.is_display_background_init:
                    self.is_display_background_init = False
                    
                    # Mettre is_display_game_menu True pour appeller self.display_background_menu dans self.draw()
                    self.is_display_game_menu = True

                elif self.is_display_game_menu:
                    self.is_display_game_menu = False
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
        background_init = pg.transform.scale(self.menu_graphics['background']['background_init'], self.screen_size)
        self.screen.blit(background_init, (0, 0)) 

    def display_background_menu(self):

        
            
        background_menu = pg.transform.scale(self.menu_graphics['background']['background_menu'], self.screen_size)
        self.screen.blit(background_menu, (0, 0))
        
        for button in self.buttons:
            self.screen.blit(button.get_image(), button.get_position())

        

    def load_saved_game_render(self):
        pass
    
    
    def options_render(self):
        pass



    def load_menu_graphics(self):

        path = 'assets/menu_sprites/'       

        return {

            'background': {
                'background_init': pg.image.load(os.path.join(path, 'Background_Init.png')),
                'background_menu': pg.image.load(os.path.join(path, 'Background_Menu.png')),
                'background_start': pg.image.load(os.path.join(path, 'Start.png')),
            },

            'logo': pg.image.load(os.path.join(path, 'Caesar3.png')),

            'buttons': {
                'start_new_career':  pg.image.load(os.path.join(path, 'start new career.png')),
                'load_saved_game': pg.image.load(os.path.join(path, 'load saved game.png')),
                'options': pg.image.load(os.path.join(path, 'options.png')),
                'exit_button': pg.image.load(os.path.join(path, 'exit.png'))
            }

            
        }

    def load_buttons(self):

        return [

            Button('start_new_career', self.menu_graphics['buttons']['start_new_career']),
            Button('load_saved_game', self.menu_graphics['buttons']['load_saved_game']),
            Button('options', self.menu_graphics['buttons']['options']),
            Button('exit_button', self.menu_graphics['buttons']['exit_button'])

        ]