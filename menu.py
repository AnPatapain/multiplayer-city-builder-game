import pygame as pg
from components import button
from events import event_manager
from game import utils

class Menu:
    def __init__(self, screen, clock):
        self.splash_screen = True
        self.active = True

        self.screen = screen
        self.clock = clock
        self.graphics = self.load_images()
        self.eventManager = event_manager.EventManager()

        # (Width, Height)
        button_size = (320, 40)

        self.button__start_new_career = button.Button("Start new career", (625, 350), button_size)
        self.button__start_new_career.on_click(self.set_inactive)

        self.button__load_saved_game = button.Button("Load saved game", (625, 400), button_size)

        self.button__options = button.Button("Options", (625, 450), button_size)

        self.button__exit = button.Button("Exit", (625, 500), button_size)
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
        self.screen.blit(self.graphics["logo"], (560, 200))

        self.button__start_new_career.display(self.screen)
        self.button__load_saved_game.display(self.screen)
        self.button__options.display(self.screen)
        self.button__exit.display(self.screen)
        pg.display.flip()


    def load_images(self):
        background = pg.image.load('assets/menu_sprites/background_menu.jpg')
        background = pg.transform.scale(background, self.screen.get_size())

        logo = pg.image.load('assets/menu_sprites/caesar3.png')
        logo = pg.transform.scale(logo, (440, 130))

        splash = pg.image.load('assets/menu_sprites/splash_screen.jpg')
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
