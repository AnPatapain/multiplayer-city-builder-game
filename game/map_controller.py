import pygame as pg

from events.event_manager import EventManager
from game.setting import OFFSET_FOR_KEY, OFFSET_FOR_MOUSE

class MapController:
    width = 1920
    height = 1080
    map_pos = [0, 0]

    

    @staticmethod
    def init_():
        EventManager.register_mouse_listener(lambda: MapController._mouse_listener())
        EventManager.register_key_listener(pg.K_DOWN, lambda: MapController.go_down(OFFSET_FOR_KEY), continuous_press=True)
        EventManager.register_key_listener(pg.K_UP, lambda: MapController.go_up(OFFSET_FOR_KEY), continuous_press=True)
        EventManager.register_key_listener(pg.K_LEFT, lambda: MapController.go_left(OFFSET_FOR_KEY), continuous_press=True)
        EventManager.register_key_listener(pg.K_RIGHT, lambda: MapController.go_right(OFFSET_FOR_KEY), continuous_press=True)
    
    @staticmethod
    def _mouse_listener():
        (x, y) = pg.mouse.get_pos()

        if x >= MapController.width * 0.999:
            MapController.go_right(OFFSET_FOR_MOUSE)
        if x <= MapController.width * 0.001:
            MapController.go_left(OFFSET_FOR_MOUSE)
        if y >= MapController.height * 0.999:
            MapController.go_down(OFFSET_FOR_MOUSE)
        if y <= MapController.width * 0.001:
            MapController.go_up(OFFSET_FOR_MOUSE)

    @staticmethod
    def go_down(offset: int):
        if MapController.map_pos[1] > -2100:
            MapController.map_pos[1] -= offset

    @staticmethod
    def go_up(offset: int):
        if MapController.map_pos[1] < 300:
            MapController.map_pos[1] += offset

    @staticmethod
    def go_left(offset: int):
        if MapController.map_pos[0] < 300:
            MapController.map_pos[0] += offset

    @staticmethod
    def go_right(offset: int):
        if MapController.map_pos[0] > -4550:
            MapController.map_pos[0] -= offset

    @staticmethod
    def get_map_pos():
        return MapController.map_pos
    
    @staticmethod
    def set_map_pos(x, y):
        '''
        Used in mini_map
        '''
        MapController.map_pos[0] = x
        MapController.map_pos[1] = y
        return MapController.map_pos

