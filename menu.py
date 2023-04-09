from enum import Enum

import pygame as pg

import backup_game
from components import button
from components.text_input import TextInput
from events.event_manager import EventManager
from game.utils import draw_text
from sounds.sounds import SoundManager
from class_types.network_commands_types import NetworkCommandsTypes

class CurrentMenu(Enum):
    SPLASHSCREEN = 0
    MAIN_MENU = 1
    LOAD_SAVE_MENU = 2
    JOIN_NETWORK_GAME_MENU = 3

class Menu:
    def __init__(self, screen):
        self.active = True

        self.current_menu = CurrentMenu.SPLASHSCREEN
        EventManager.set_any_input(self.go_to_main_menu)

        self.screen = screen
        self.graphics = self.load_images()
        self.sound_manager = SoundManager()

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
        self.button__load_saved_game.on_click(self.go_to_loading_game_menu)


        self.button__exit = button.Button((button_start, 500), button_size,
                                                      image=pg.image.load('assets/menu_sprites/exit.png').convert(),
                                                      image_hover=pg.image.load('assets/menu_sprites/exit_hover.png').convert())
        self.button__exit.on_click(exit)

        self.save1 = button.Button((button_start, 300), button_size, text="Save1", center_text=True)
        self.save1.on_click(self.set_inactive)

        self.save2 = button.Button((button_start, 350), button_size, text="Save2", center_text=True)
        #self.save2.on_click(self.load_save)

        self.save3 = button.Button((button_start, 400), button_size, text="Save3", center_text=True)
        #self.save3.set_disabled(True)

        self.save4 = button.Button((button_start, 450), button_size, text="Save4", center_text=True)
        #self.save4.on_click(exit)

        self.come_back_to_main_menu = button.Button((button_start, 500), (50,45), text="<", center_text=True)
        self.come_back_to_main_menu.on_click(self.go_to_main_menu)

        self.button__multiplayer = button.Button((button_start, 450), button_size, text="Multiplayer",center_text=True)
        self.button__multiplayer.on_click(self.go_to_online_menu)

        self.button__connect = button.Button((button_start, 400), button_size, text="Connect",center_text=True)
        self.button__connect.on_click(self.connect_to_c_client)

        self.input_ip = TextInput((button_start,300 ), (320, 30), placeholder="Enter the ip address.")
        self.input_user = TextInput((button_start, 350), (320, 30), placeholder="Enter your username.", focused=False)
        self.saved_game = False

        # pg.mixer.music.load('sounds/wavs/ROME4.WAV')
        # pg.mixer.music.set_volume(0.6)
        # pg.mixer.music.play(0, 0, 2000)




    def run(self, already_launched_once: bool):
        if already_launched_once:
            self.go_to_main_menu()
        while self.is_active():
            EventManager.handle_events()
            self.affichage()
        return


    def affichage(self):
        self.screen.blit(self.graphics["background"], (0, 0))
        #self.sound_manager.play('menu_demarrer')

        rect_size = (500, 400)
        rect_pos = ((self.screen.get_size()[0]/2) - (rect_size[0]/2), 180)
        rect = pg.Rect(rect_pos, rect_size)
        pg.draw.rect(self.screen, (60, 40, 25), rect)

        match self.current_menu:
            case CurrentMenu.SPLASHSCREEN:
                self.show_splashscreen()
            case CurrentMenu.MAIN_MENU:
                self.show_main_menu()
            case CurrentMenu.LOAD_SAVE_MENU:
                self.show_save_menu()
            case CurrentMenu.JOIN_NETWORK_GAME_MENU:
                self.show_online_menu()
        pg.display.flip()


    def show_splashscreen(self):
        self.screen.blit(self.graphics["splash"], (0, 0))


    def show_main_menu(self):
        logo_start = (self.screen.get_size()[0]/2) - (self.graphics["logo"].get_size()[0]/2)
        self.screen.blit(self.graphics["logo"], (logo_start, 200))
        self.button__start_new_career.display(self.screen)
        self.button__load_saved_game.display(self.screen)
        self.button__multiplayer.display(self.screen)
        self.button__exit.display(self.screen)


    def show_save_menu(self):
        logo_start = (self.screen.get_size()[0]/2) - (self.graphics["logo"].get_size()[0]/2)
        draw_text("Load a City", self.screen,(logo_start+70, 200), color=(255, 255, 200))
        print(backup_game.list_fichiers)
        self.save1.display(self.screen)
        self.save2.display(self.screen)
        self.save3.display(self.screen)
        self.save4.display(self.screen)
        self.come_back_to_main_menu.display(self.screen)

    def show_online_menu(self):
            draw_text("Play Online with other players!", self.screen, (775, 225), color=(255, 255, 200))
            self.button__connect.display(self.screen)
            self.input_ip.display(self.screen)
            self.input_user.display(self.screen)
            self.come_back_to_main_menu.display(self.screen)



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
        pg.mixer.music.stop()

    def event_main_menu(self):
        EventManager.reset()
        EventManager.register_component(self.button__start_new_career)
        EventManager.register_component(self.button__load_saved_game)
        EventManager.register_component(self.button__multiplayer)
        EventManager.register_component(self.button__exit)
        EventManager.register_key_listener(pg.K_ESCAPE, exit)

    def event_load_menu(self):
        EventManager.reset()
        EventManager.register_component(self.save1)
        EventManager.register_component(self.save2)
        EventManager.register_component(self.save3)
        EventManager.register_component(self.save4)
        EventManager.register_component(self.come_back_to_main_menu)
        EventManager.register_key_listener(pg.K_ESCAPE, self.go_to_main_menu)

    def event_online_menu(self):
        EventManager.reset()
        EventManager.register_component(self.input_ip)
        EventManager.register_component(self.input_user)
        EventManager.register_component(self.button__connect)
        EventManager.register_component(self.come_back_to_main_menu)
        EventManager.register_key_listener(pg.K_ESCAPE, self.go_to_main_menu)





    def load_save(self):
        self.set_inactive()

    def go_to_loading_game_menu(self):
        self.event_load_menu()
        self.current_menu = CurrentMenu.LOAD_SAVE_MENU

    def go_to_online_menu(self):
        self.event_online_menu()
        self.current_menu = CurrentMenu.JOIN_NETWORK_GAME_MENU

    def go_to_main_menu(self):
        self.event_main_menu()
        self.current_menu = CurrentMenu.MAIN_MENU

    def connect_to_c_client(self):
        from network_system.system_layer.read_write import SystemInterface

        username = self.input_user.get_text()
        ip = self.input_ip.get_text()

        si = SystemInterface.get_instance()
        si.set_ip(ip)
        si.run_subprocess()
        si.send_message(NetworkCommandsTypes.ASK_SAVE,0,None,encode=False)
        si.recieve_game_save()
        self.saved_game = True
        self.set_inactive()

    def is_load_save(self) -> bool:
        return self.saved_game

