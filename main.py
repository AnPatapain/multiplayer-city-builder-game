import pygame as pg
from game.game import Game
from game.setting import SCREEN_HEIGHT, SCREEN_WIDTH
from menu.menu import Menu

def main():
    is_game_run = True
    is_playing = True

    pg.init()
    # screen = pg.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT]) # -> Surface instance
    screen = pg.display.set_mode((0,0), pg.FULLSCREEN)
    pg.event.set_grab(True)
    clock = pg.time.Clock()
    game = Game(screen, clock)

    menu = Menu(screen, clock)
    
    while is_game_run:

        # menu.run()

        while is_playing:
            game.run()


if __name__ == "__main__":
    main()