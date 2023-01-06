import pygame as pg

from events.event_manager import EventManager
from game.game import Game
from menu import Menu
from game.textures import Textures


def main():
    is_game_run = True
    is_playing = True

    pg.init()
    # screen = pg.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT]) # -> Surface instance
    screen = pg.display.set_mode((1920,1080), pg.FULLSCREEN)
    pg.display.set_caption("Taboule Raza")
    pg.display.set_icon(pg.image.load('assets/menu_sprites/game_icon.png'))
    pg.event.set_grab(True)
    clock = pg.time.Clock()
    menu = Menu(screen, clock)
    Textures.init(screen)

    while menu.is_active():
        menu.run()

    # Clear buttons from the menu
    EventManager.reset()
    game = Game(screen, clock)
    while is_game_run:

        while is_playing:

            game.run()


if __name__ == "__main__":
    main()
