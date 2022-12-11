import pygame as pg

from events.event_manager import EventManager
from game.setting import OFFSET_FOR_KEY, OFFSET_FOR_MOUSE

class MapController:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.map_pos = [0, 0]

        EventManager.register_mouse_listener(self._mouse_listener)
        EventManager.register_key_listener(pg.K_DOWN, lambda: self.go_down(OFFSET_FOR_KEY), continuous_press=True)
        EventManager.register_key_listener(pg.K_UP, lambda: self.go_up(OFFSET_FOR_KEY), continuous_press=True)
        EventManager.register_key_listener(pg.K_LEFT, lambda: self.go_left(OFFSET_FOR_KEY), continuous_press=True)
        EventManager.register_key_listener(pg.K_RIGHT, lambda: self.go_right(OFFSET_FOR_KEY), continuous_press=True)

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
    
    def set_map_pos(self, x, y):
        '''
        Used in mini_map
        '''
        self.map_pos[0] = x
        self.map_pos[1] = y
        return self.map_pos
