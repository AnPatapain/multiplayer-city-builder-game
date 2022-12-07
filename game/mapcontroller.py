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
        self.event_manager.register_key_listener(pg.K_DOWN, self._down_arrow, continuous_press=True)
        self.event_manager.register_key_listener(pg.K_UP, self._up_arrow, continuous_press=True)
        self.event_manager.register_key_listener(pg.K_LEFT, self._left_arrow, continuous_press=True)
        self.event_manager.register_key_listener(pg.K_RIGHT, self._right_arrow, continuous_press=True)

    def _mouse_listener(self):
        mouse_position = pg.mouse.get_pos()
        (x, y) = mouse_position

        if x >= self.width * 0.97:
            if self.in_constraint(self.map_pos[0] - OFFSET_FOR_KEY, self.map_pos[1]):
                self.map_pos[0] -= OFFSET_FOR_MOUSE

        if x <= self.width * 0.03:
            if self.in_constraint(self.map_pos[0] + OFFSET_FOR_KEY, self.map_pos[1]):
                self.map_pos[0] += OFFSET_FOR_MOUSE

        if y >= self.height * 0.97:
            if self.in_constraint(self.map_pos[0], self.map_pos[1] - OFFSET_FOR_KEY):
                self.map_pos[1] -= OFFSET_FOR_MOUSE
        if y <= self.width * 0.03:
            if self.in_constraint(self.map_pos[0], self.map_pos[1] + OFFSET_FOR_KEY):
                self.map_pos[1] += OFFSET_FOR_MOUSE

    def _down_arrow(self):
        if self.in_constraint(self.map_pos[0], self.map_pos[1] - OFFSET_FOR_KEY):
            self.map_pos[1] -= OFFSET_FOR_KEY

    def _up_arrow(self):
        if self.in_constraint(self.map_pos[0], self.map_pos[1] + OFFSET_FOR_KEY):
            self.map_pos[1] += OFFSET_FOR_KEY

    def _left_arrow(self):
        if self.in_constraint(self.map_pos[0] + OFFSET_FOR_KEY, self.map_pos[1]):
            self.map_pos[0] += OFFSET_FOR_KEY

    def _right_arrow(self):
        if self.in_constraint(self.map_pos[0] - OFFSET_FOR_KEY, self.map_pos[1]):
            self.map_pos[0] -= OFFSET_FOR_KEY

    def get_map_pos(self):
        return self.map_pos

    def in_constraint(self, map_pos_x, map_pos_y):
        in_constraint_x = -DEFAULT_SURFACE_WIDTH <= map_pos_x <= 0
        in_constraint_y = -DEFAULT_SURFACE_HEIGHT + self.height <= map_pos_y <= self.height*0.04
        if in_constraint_x and in_constraint_y:
            return True