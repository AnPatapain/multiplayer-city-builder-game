import pygame as pg

import backup_game
from events.event_manager import EventManager
from game.game import Game
from menu import Menu
from game.textures import Textures


def main():
    is_game_run = True
    is_playing = True

    pg.init()
    screen = pg.display.set_mode((1920, 1080), pg.FULLSCREEN)
    pg.display.set_caption("Taboule Raza")
    pg.display.set_icon(pg.image.load('assets/menu_sprites/game_icon.png'))
    pg.event.set_grab(True)
    menu = Menu(screen)
    Textures.init(screen)

    while menu.is_active():
        menu.run()

    # Clear buttons from the menu
    EventManager.reset()
    game = Game(screen)

    # Save load, need to be here to load save after init game
    if menu.get_save_loading():
        backup_game.load_game("save.bin")

    while is_game_run:

        while is_playing:

            game.run()


if __name__ == "__main__":
    main()
