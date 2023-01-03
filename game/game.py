import pygame as pg

from events.event_manager import EventManager
from sounds.sounds import SoundManager
from .world import World
from .utils import draw_text
from .map_controller import MapController
from .panel import Panel
from .setting import *
from .game_controller import GameController


class Game:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.game_controller = GameController.get_instance()
        self.width, self.height = self.screen.get_size()

        # sound manager
        self.sound_manager = SoundManager()

        # panel has two sub_panel: ressource_panel for displaying Dn, Populations, etc and building_panel
        # for displaying available building in game
        self.panel = Panel(self.width, self.height)

        # World contains populations or graphical objects like buildings, trees, grass
        self.world = World(GRID_SIZE, GRID_SIZE, self.width, self.height, self.panel)

        MapController.init_()

        # Exit the game when pressing <esc>
        EventManager.register_key_listener(pg.K_ESCAPE, exit)
        # Calls the event_handler of the World
        EventManager.add_hooked_function(self.world.event_handler, MapController.get_map_pos())

    # Game Loop
    def run(self):
        self.clock.tick(50)
        EventManager.handle_events()
        gc = GameController.get_instance()
        for walker in gc.walkers:
            walker.update()
        self.update()
        self.draw()

    def draw(self):
        self.screen.fill((0, 0, 0))

        self.world.draw(self.screen)
        self.panel.draw(self.screen)

        draw_text('fps={}'.format(round(self.clock.get_fps())), self.screen, (self.width - 120, 10), size=42)
        draw_text('denier {}'.format(self.game_controller.get_denier()), self.screen, (self.width - 905, 10), size=42)

        pg.display.flip()

    def update(self):
        self.panel.update()
        self.world.update()
