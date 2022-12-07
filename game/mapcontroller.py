import pygame as pg

from events.event_manager import EventManager
from .setting import OFFSET_FOR_KEY, OFFSET_FOR_MOUSE
from .setting import DEFAULT_SURFACE_HEIGHT, DEFAULT_SURFACE_WIDTH

class MapController:
    def __init__(self, width: int, height: int, event_manager: EventManager):
        self.width = width
        self.height = height
        self.map_pos = [0, 0]
        self.event_manager = event_manager

        self.event_manager.register_mouse_listener(self._mouse_listener)
        self.event_manager.register_key_listener(pg.K_DOWN, lambda: self.go_down(OFFSET_FOR_KEY), continuous_press=True)
        self.event_manager.register_key_listener(pg.K_UP, lambda: self.go_up(OFFSET_FOR_KEY), continuous_press=True)
        self.event_manager.register_key_listener(pg.K_LEFT, lambda: self.go_left(OFFSET_FOR_KEY), continuous_press=True)
        self.event_manager.register_key_listener(pg.K_RIGHT, lambda: self.go_right(OFFSET_FOR_KEY), continuous_press=True)

    def _mouse_listener(self):
        (x, y) = pg.mouse.get_pos()

        if x >= self.width * 0.97:
            self.go_right(OFFSET_FOR_MOUSE)
        if x <= self.width * 0.03:
            self.go_left(OFFSET_FOR_MOUSE)
        if y >= self.height * 0.97:
            self.go_down(OFFSET_FOR_MOUSE)
        if y <= self.width * 0.03:
            self.go_up(OFFSET_FOR_MOUSE)

    def go_down(self, offset: int):
        if self.map_pos[1] > -2100:
            self.map_pos[1] -= offset

    def go_up(self, offset: int):
        if self.map_pos[1] < 300:
            self.map_pos[1] += offset

    def go_left(self, offset: int):
        if self.map_pos[0] < 300:
            self.map_pos[0] += offset

    def go_right(self, offset: int):
        if self.map_pos[0] > -4550:
            self.map_pos[0] -= offset

    def get_map_pos(self):
        return self.map_pos

    def in_constraint(self, map_pos_x, map_pos_y):
        in_constraint_x = -DEFAULT_SURFACE_WIDTH <= map_pos_x <= 0
        in_constraint_y = -DEFAULT_SURFACE_HEIGHT + self.height <= map_pos_y <= self.height*0.04
        if in_constraint_x and in_constraint_y:
            return True