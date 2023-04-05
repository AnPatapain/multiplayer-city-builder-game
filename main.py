import pygame as pg
import backup_game
from events.event_manager import EventManager
from game.game import Game
from menu import Menu
from game.textures import Textures



def main():
    pg.init()
    # screen = pg.display.set_mode((1920, 1080), pg.FULLSCREEN)
    screen = pg.display.set_mode((1220, 680))
    pg.display.set_caption("Taboule Raza")
    pg.display.set_icon(pg.image.load('assets/menu_sprites/game_icon.png'))
    curseur = pg.cursors.Cursor((0, 0), pg.image.load("assets/C3_sprites/system/Arrow.png"))
    pg.mouse.set_cursor(curseur)
    pg.event.set_grab(True)

    Textures.init(screen)

    # Save load, need to be here to load save after init game
    # Not implemented yet
    # if menu.get_save_loading():
    #     backup_game.load_game("save.bin")

    already_launched_once = False

    while True:
        menu = Menu(screen)
        menu.run(already_launched_once)
        del menu

        already_launched_once = True


        # Clear buttons from the menu
        EventManager.reset()
        pg.mixer.music.stop()


        game = Game(screen)
        game.run()
        del game

        EventManager.reset()
        pg.mixer.music.stop()


if __name__ == "__main__":
    main()
