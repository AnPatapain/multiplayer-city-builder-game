import pygame as pg
import os

class Menu:
    
    def __init__(self, screen):
        
        self.interface_menu = False # To keep the game run if we click the position of general button like "exit" in background1
        self.images = self.load_images()
        self.screensize = screen.get_size()
        

    def load_images(self):

        path = 'assets/menu_sprites/'

        # load_saved_game = pygame.image.load('assets/menu_sprites/load saved game.png')
        # options = pygame.image.load('assets/menu_sprites/options.png')
        # exit_button = pygame.image.load('assets/menu_sprites/exit.png')       

        return {
            'background1': pg.image.load(os.path.join(path, 'Background_Init.png')),
            'background2': pg.image.load(os.path.join(path, 'Background_Menu.png')),
            'background3': pg.image.load(os.path.join(path, 'Start.png')),

            'logo': pg.image.load(os.path.join(path, 'Caesar3.png')),
            'start_new_career':  pg.image.load(os.path.join(path, 'start new career.png')),
            'load_saved_game': pg.image.load(os.path.join(path, 'load saved game.png')),
            'options': pg.image.load(os.path.join(path, 'options.png')),
            'exit_button': pg.image.load(os.path.join(path, 'exit.png'))
        }

    def survole(self, bouton, pos):
        if bouton.x < pos[0] < bouton.x + bouton.width:
            if bouton.y < pos[1] < bouton.y + bouton.height:
                return True
        return False

    def mouse_event_handler(self, event):

        if event.type == pg.MOUSEMOTION:
            #boutons_dynamiques(start_new_career, exit_button)
            if self.survole(start_new_career_rect, pos):
                start_new_career = pg.image.load('assets/menu_sprites/start new career mouse on.png')
            elif not self.survole(start_new_career_rect, pos):
                start_new_career = pg.image.load('assets/menu_sprites/start new career.png')
            if self.survole(exit_rect, pos):
                exit_button = pg.image.load('assets/menu_sprites/exit mouse on.png')
            elif not self.survole(exit_rect, pos):
                exit_button = pg.image.load('assets/menu_sprites/exit.png')
        if event.type == pg.MOUSEBUTTONDOWN:
            if not interface_menu:
                # background = pg.image.load('assets/menu_sprites/Background_Menu.png')
                # background = pg.transform.scale(background, x)
                background = pg.transform.scale(self.images['background2'], self.screensize)
                interface_menu = True
            elif interface_menu:
                if exit_rect.collidepoint(event.pos):
                    launched = False
                    pg.quit()
                if start_new_career_rect.collidepoint(event.pos):
                    interface_menu = False
                    background = pg.transform.scale(self.images['background3'], self.screensize)

        
        # if event.key == pg.K_DOWN:
        #     self.map_position[1] = self.map_position[1] - self.offset_for_key
        # if event.key == pg.K_UP:
        #     self.map_position[1] = self.map_position[1] + self.offset_for_key
        # if event.key == pg.K_LEFT:
        #     self.map_position[0] = self.map_position[0] + self.offset_for_key
        # if event.key == pg.K_RIGHT:
        #     self.map_position[0] = self.map_position[0] - self.offset_for_key

    def scale_image(image, size): pass

    
