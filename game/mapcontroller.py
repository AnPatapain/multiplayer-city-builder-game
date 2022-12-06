import pygame as pg

from events.event_manager import EventManager
from .setting import OFFSET_FOR_KEY, OFFSET_FOR_MOUSE

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
            self.map_pos[0] -= OFFSET_FOR_MOUSE
        if x <= self.width * 0.03:
            self.map_pos[0] += OFFSET_FOR_MOUSE
        if y >= self.height * 0.97:
            self.map_pos[1] -= OFFSET_FOR_MOUSE
        if y <= self.width * 0.03:
            self.map_pos[1] += OFFSET_FOR_MOUSE

    def _down_arrow(self):
        self.map_pos[1] -= OFFSET_FOR_KEY

    def _up_arrow(self):
        self.map_pos[1] += OFFSET_FOR_KEY

    def _left_arrow(self):
        self.map_pos[0] += OFFSET_FOR_KEY

    def _right_arrow(self):
        self.map_pos[0] -= OFFSET_FOR_KEY

    def get_map_pos(self):
        return self.map_pos
