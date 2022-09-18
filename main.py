import pygame as pg
from game.game import Game


def main():
    game_run = True
    is_playing = True

    pg.init()
    screen = pg.display.set_mode((0, 0), pg.FULLSCREEN) # return surface instance
    clock = pg.time.Clock()

    game = Game(screen, clock)
    while game_run:
        # display menu
        while is_playing:
            #game loop (Draw screen -> event handling -> update state)
            game.run()


if __name__ == "__main__":
    main()