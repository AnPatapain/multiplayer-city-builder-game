import pygame as pg

from events.event_manager import EventManager
from .world import World
from .utils import draw_text
from .mapcontroller import MapController
from .panel import Panel
from .setting import *
from .mini_map import MiniMap

from events import event_manager


class Game:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.width, self.height = self.screen.get_size()

        # event_manager handles every event (mouse & keyboard input) of the game
        self.event_manager = EventManager()

        # map_controller update position of surface that the map blited on according to mouse position or key event
        self.map_controller = MapController(self.width, self.height, self.event_manager)

        # panel has two sub_panel: ressource_panel for displaying Dn, Populations, etc and building_panel
        # for displaying available building in game
        self.panel = Panel(self.width, self.height, self.event_manager)

        # Mini_Map
        self.mini_map = MiniMap(self.screen, self.width, self.height)

        # World contains populations or graphical objects like buildings, trees, grass
        self.world = World(NUMS_GRID_X, NUMS_GRID_Y, self.width, self.height, self.panel)

        # Exit the game when pressing <esc>
        self.event_manager.register_key_listener(pg.K_ESCAPE, exit)
        # Calls the event_handler of the World
        self.event_manager.add_hooked_function(self.world.event_handler, self.map_controller.get_map_pos())

    # Game Loop
    def run(self):
        self.clock.tick(60)
        self.event_manager.handle_events()
        
        self.update()
        self.draw()

    def draw(self):
        self.screen.fill((0, 0, 0))

        self.world.draw(self.screen, self.map_controller.get_map_pos())

        self.panel.draw(self.screen)

        self.mini_map.draw(self.map_controller.get_map_pos())

        draw_text('fps={}'.format(round(self.clock.get_fps())), self.screen, (self.width - 200, 20), size=42)
                
        pg.display.flip()

    def update(self):
        self.panel.update()
        self.world.update(self.map_controller.get_map_pos())
