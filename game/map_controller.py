import pygame as pg

class Map_controller:

    def __init__(self, width, height):

        self.width = width
        self.height = height
        self.map_pos = [0, 0]
        self.offset_for_mouse = 20
        self.offset_for_key = 50

    def event_handler(self, event):
        
        if event.key == pg.K_DOWN:
            self.map_pos[1] = self.map_pos[1] - self.offset_for_key
        if event.key == pg.K_UP:
            self.map_pos[1] = self.map_pos[1] + self.offset_for_key
        if event.key == pg.K_LEFT:
            self.map_pos[0] = self.map_pos[0] + self.offset_for_key
        if event.key == pg.K_RIGHT:
            self.map_pos[0] = self.map_pos[0] - self.offset_for_key
    
    def update_map_pos(self):

        mouse_position = pg.mouse.get_pos()
        (x, y) = mouse_position
        
        if x >= self.width * 0.97:
            self.map_pos[0] = self.map_pos[0] - self.offset_for_mouse
        if x <= self.width * 0.03:
            self.map_pos[0] = self.map_pos[0] + self.offset_for_mouse
        if y >= self.height * 0.97:
            self.map_pos[1] = self.map_pos[1] - self.offset_for_mouse
        if y <= self.width * 0.03:
            self.map_pos[1] = self.map_pos[1] + self.offset_for_mouse

    def get_map_pos(self): return self.map_pos