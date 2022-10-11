import pygame as pg
from game.game import Game
from menu import Menu
from game.setting import SCREEN_HEIGHT, SCREEN_WIDTH


def main():
    is_game_run = True
    is_playing = True

    pg.init()
    # screen = pg.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT]) # -> Surface instance
    screen = pg.display.set_mode((0,0), pg.FULLSCREEN)
    pg.display.set_caption("Taboule Raza")
    pg.display.set_icon(pg.image.load('assets/menu_sprites/game_icon.png'))
    pg.event.set_grab(True)
    clock = pg.time.Clock()
    menu = Menu(screen, clock)

    while menu.is_active():
        menu.run()

    game = Game(screen, clock)
    while is_game_run:
        # in case player pause the game for reading instruction or view game menu
        while is_playing:
            #game loop (Draw screen -> event handling -> update state)
            game.run()


if __name__ == "__main__":
    main()
