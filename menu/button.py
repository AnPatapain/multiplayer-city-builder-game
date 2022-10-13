import pygame as pg


DEFAULT_TOP = 0
DEFAULT_LEFT = 0

DEFAULT_MARGIN_TOP = 0
class Button:
    
    def __init__( self, name, image, position=(DEFAULT_LEFT, DEFAULT_TOP) ):
        self.name = name
        self.image = image
        self.position = (DEFAULT_LEFT, DEFAULT_TOP)

        self.rect = pg.Rect(self.position[0], self.position[1], self.image.get_width(), self.image.get_height())
        self.margin_top = DEFAULT_MARGIN_TOP
        pass

    def check_button(self):
        pass
    
    def get_button_size(self):
        return self.image.get_size()

    def get_image(self):
        return self.image
    
    def set_image(self, image):
        self.image = image

    def get_position(self):
        return self.position

    def set_position(self, pos):
        self.position = pos
        

    def set_margin_top(self, margin_top):
        self.margin_top = margin_top
    
    def get_margin_top(self):
        return self.margin_top