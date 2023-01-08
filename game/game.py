import time

import numpy
import pygame as pg

from events.event_manager import EventManager
from sounds.sounds import SoundManager
from .world import World
from .utils import draw_text
from .map_controller import MapController
from .panel import Panel
from .game_controller import GameController


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.paused = False
        self.game_controller = GameController.get_instance()
        self.width, self.height = self.screen.get_size()

        # sound manager
        self.sound_manager = SoundManager()

        # panel has two sub_panel: ressource_panel for displaying Dn, Populations, etc and building_panel
        # for displaying available building in game
        self.panel = Panel(self.width, self.height)

        # World contains populations or graphical objects like buildings, trees, grass
        self.world = World(self.width, self.height, self.panel)

        MapController.init_()

        # Exit the game when pressing <esc>
        EventManager.register_key_listener(pg.K_ESCAPE, exit)
        # Calls the event_handler of the World
        EventManager.add_hooked_function(self.world.event_handler)
        EventManager.register_key_listener(pg.K_SPACE, self.toogle_pause)

    # Game Loop
    def run(self):
        fps_moyen = [0]
        ms_waited = 0

        while True:

            # We need to recalculate it every time, since it can change
            targeted_ticks_per_seconds = self.game_controller.get_current_speed() * 50
            ms_between_ticks = 1000 / targeted_ticks_per_seconds

            start_logic = time.process_time_ns()
            if not self.paused:
                self.game_controller.update()
                for walker in GameController.get_instance().walkers:
                    walker.update()

            end_logic = time.process_time_ns()
            logic_diff = (end_logic - start_logic) / 1000000
            ms_waited += logic_diff

            while ms_waited < ms_between_ticks:
                start_render = time.process_time_ns()
                EventManager.handle_events()

                self.world.update()
                self.panel.update()
                self.draw(int(numpy.average(fps_moyen)))
                end_render = time.process_time_ns()
                time_diff = (end_render - start_render) / 1000000

                if len(fps_moyen) > 100:
                    fps_moyen.pop(0)
                fps_moyen.append(1000/time_diff)
                ms_waited += time_diff


            ms_waited = ms_waited - ms_between_ticks



    def toogle_pause(self):
        self.paused = not self.paused

    def draw(self, fps):
        self.screen.fill((0, 0, 0))
        self.world.draw(self.screen)
        self.panel.draw(self.screen)
        month_number = self.game_controller.get_actual_month()

        draw_text('fps={}'.format(fps), self.screen, (self.width - 120, 10), size=42)
        draw_text('Denier  {}'.format(self.game_controller.get_denier()), self.screen, (self.width - 905, 10), size=42)
        draw_text('Pop  {}'.format(self.game_controller.get_actual_citizen()), self.screen, (self.width - 1200, 10), size=42)
        draw_text('{} '.format(self.game_controller.get_month(month_number)), self.screen, (self.width - 590, 10), color=pg.Color(255, 255, 0), size=42)
        draw_text('{} BC'.format(self.game_controller.get_actual_year()), self.screen, (self.width - 500, 10), color=pg.Color(255, 255, 0), size=42)

        pg.display.flip()


