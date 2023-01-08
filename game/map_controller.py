import pygame as pg

from events.event_manager import EventManager
from game.setting import OFFSET_FOR_KEY, OFFSET_FOR_MOUSE

class MapController:
    width = 1920
    height = 1080
    map_pos = [0, 0]

    start_moving_coord = None
    start_moving_pos = None

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

        wheel_pressed = pg.mouse.get_pressed()[1]
        if MapController.start_moving_coord is None and wheel_pressed:
            MapController.start_moving_coord = (x, y)
            MapController.start_moving_pos = MapController.map_pos.copy()

        if MapController.start_moving_coord and wheel_pressed:
            diff_x = MapController.start_moving_coord[0] - x
            diff_y = MapController.start_moving_coord[1] - y

            MapController.set_map_pos(
                MapController.start_moving_pos[0] - diff_x,
                MapController.start_moving_pos[1] - diff_y
            )

        if not wheel_pressed and MapController.start_moving_coord:
            MapController.start_moving_coord = None
            MapController.start_moving_pos = None

    @staticmethod
    def go_down(offset: int):
        MapController.set_map_pos(MapController.map_pos[0], MapController.map_pos[1] - offset)

    @staticmethod
    def go_up(offset: int):
        MapController.set_map_pos(MapController.map_pos[0], MapController.map_pos[1] + offset)

    @staticmethod
    def go_left(offset: int):
        MapController.set_map_pos(MapController.map_pos[0] + offset, MapController.map_pos[1])

    @staticmethod
    def go_right(offset: int):
        MapController.set_map_pos(MapController.map_pos[0] - offset, MapController.map_pos[1])

    @staticmethod
    def get_map_pos():
        return MapController.map_pos
    
    @staticmethod
    def set_map_pos(x, y):
        if -6100 < MapController.map_pos[0] + x < 300:
            MapController.map_pos[0] = x

        if -2800 < MapController.map_pos[1] + y < 300:
            MapController.map_pos[1] = y

        return MapController.map_pos

