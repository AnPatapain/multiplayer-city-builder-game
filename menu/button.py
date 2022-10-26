import pygame as pg


DEFAULT_TOP = 0
DEFAULT_LEFT = 0

DEFAULT_MARGIN_TOP = 0
class Button:
    
    def __init__( self, name, image):
        self.name = name
        self.image = image
        self.position = (DEFAULT_LEFT, DEFAULT_TOP)

        # self.rect = pg.Rect(left=DEFAULT_LEFT, top=DEFAULT_TOP, width=self.image.get_size()[0], height=self.image.get_size()[1])
        self.rect = None
        self.margin_top = DEFAULT_MARGIN_TOP
        pass

    def check_button(self):
        action = False

        pos = pg.mouse.get_pos()

        mouse_action = pg.mouse.get_pressed()

        if self.rect.collidepoint(pos):
            if mouse_action[0]:
                action = True

        return action
    
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

    def set_rect(self, pos, size):
        self.rect = pg.Rect(pos[0], pos[1], size[0], size[1])
    
    def get_margin_top(self):
        return self.margin_top

    def get_name(self):
        return self.name