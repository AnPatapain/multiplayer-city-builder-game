import pygame as pg

import sounds.sounds
from components import button
from events import event_manager
from sounds import sounds
from game import game


class Menu:
    def __init__(self, screen, clock):
        self.splash_screen = True
        self.active = True

        self.screen = screen
        self.clock = clock
        self.graphics = self.load_images()
        self.eventManager = event_manager.EventManager()
        self.sound_manager = sounds.SoundManager()

        # (Width, Height)
        button_size = (322, 32)
        button_start = (self.screen.get_size()[0]/2) - (button_size[0]/2)

        self.button__start_new_career = button.Button((button_start, 350),button_size,
                                                      image=pg.image.load('assets/menu_sprites/start.png').convert(),
                                                      image_hover=pg.image.load('assets/menu_sprites/start_hover.png').convert())
        self.button__start_new_career.on_click(self.set_inactive)

        self.button__load_saved_game = button.Button((button_start, 400), button_size,
                                                      image=pg.image.load('assets/menu_sprites/load saved game.png').convert(),
                                                      image_hover=pg.image.load('assets/menu_sprites/load_saved_game_mouse_on.png').convert())

        self.button__options = button.Button((button_start, 450), button_size,
                                                      image=pg.image.load('assets/menu_sprites/options.png').convert(),
                                                      image_hover=pg.image.load('assets/menu_sprites/options_mouse_on.png').convert())
        #self.button__options.set_disabled(True)

        self.button__exit = button.Button((button_start, 500), button_size,
                                                      image=pg.image.load('assets/menu_sprites/exit.png').convert(),
                                                      image_hover=pg.image.load('assets/menu_sprites/exit_hover.png').convert())
        self.button__exit.on_click(exit)

        self.eventManager.register_component(self.button__start_new_career)\
            .register_component(self.button__load_saved_game)\
            .register_component(self.button__options)\
            .register_component(self.button__exit)

        self.eventManager.set_any_input(self.skip_splashscreen)
        self.screen.blit(self.graphics["splash"], (0, 0))
        pg.display.flip()


    def run(self):
        self.clock.tick(60)
        self.eventManager.handle_events()

        if self.is_splashscreen_skipped():
            self.affichage()


    def affichage(self):
        self.screen.blit(self.graphics["background"], (0, 0))
        self.sound_manager.play('menu_demarrer')

        logo_start = (self.screen.get_size()[0]/2) - (self.graphics["logo"].get_size()[0]/2)
        self.screen.blit(self.graphics["logo"], (logo_start, 200))

        self.button__start_new_career.display(self.screen)
        self.button__load_saved_game.display(self.screen)
        self.button__options.display(self.screen)
        self.button__exit.display(self.screen)
        pg.display.flip()


    def load_images(self):
        background = pg.image.load('assets/menu_sprites/background_menu.jpg').convert()
        background = pg.transform.scale(background, self.screen.get_size())

        logo = pg.image.load('assets/menu_sprites/caesar3.png').convert_alpha()
        logo = pg.transform.scale(logo, (440, 130))

        splash = pg.image.load('assets/menu_sprites/splash_screen.jpg').convert()
        splash = pg.transform.scale(splash, self.screen.get_size())


        return {
            'background': background,
            'logo': logo,
            'splash': splash

        }

    def is_active(self):
        return self.active

    def set_inactive(self):
        self.active = False

    def skip_splashscreen(self):
        self.eventManager.clear_any_input()
        self.splash_screen = False

    def is_splashscreen_skipped(self):
        return not self.splash_screen
