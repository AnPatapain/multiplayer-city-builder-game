import pygame as pg

from events.event_manager import EventManager
from sounds.sounds import SoundManager
from .world import World
from .utils import draw_text
from .mapcontroller import MapController
from .panel import Panel
from .setting import *


class Game:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.width, self.height = self.screen.get_size()

        # sound manager
        self.sound_manager = SoundManager()


        # panel has two sub_panel: ressource_panel for displaying Dn, Populations, etc and building_panel
        # for displaying available building in game
        self.panel = Panel(self.width, self.height, self.map_controller)

        # World contains populations or graphical objects like buildings, trees, grass
        self.world = World(NUMS_GRID_X, NUMS_GRID_Y, self.width, self.height, self.panel)

        # Exit the game when pressing <esc>
        EventManager.register_key_listener(pg.K_ESCAPE, exit)
        # Calls the event_handler of the World
        EventManager.add_hooked_function(self.world.event_handler, self.map_controller.get_map_pos())

    # Game Loop
    def run(self):
        self.clock.tick(60)
        EventManager.handle_events()
        
        self.update()
        self.draw()

    def draw(self):
        self.screen.fill((0, 0, 0))

        self.world.draw(self.screen, MapController.get_map_pos())

        self.panel.draw(self.screen)

        draw_text('fps={}'.format(round(self.clock.get_fps())), self.screen, (self.width - 200, 20), size=42)

        pg.display.flip()

    def update(self):
        self.panel.update()
        self.world.update(MapController.get_map_pos())
