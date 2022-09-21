import pygame as pg
from game.game import Game
from game.setting import SCREEN_HEIGHT, SCREEN_WIDTH


def main():
    is_game_run = True
    is_playing = True

    pg.init()
    screen = pg.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT]) # -> Surface instance
    clock = pg.time.Clock()
    game = Game(screen, clock)
    
    while is_game_run:
        # in case player pause the game for reading instruction or view game menu
        while is_playing:
            #game loop (Draw screen -> event handling -> update state)
            game.run()


if __name__ == "__main__":
    main()