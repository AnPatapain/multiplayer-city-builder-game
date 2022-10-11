import pygame as pg
from game import utils

TEXT_COLOR = pg.Color(27, 27, 27)
BASE_COLOR = pg.Color(154, 146, 121)
HOVER_COLOR = pg.Color(139, 131, 106)

class Button:
    def __init__(self, text, pos, size):
        self.text = text
        self.color = BASE_COLOR
        self.rect = pg.Rect(pos, size)
        self.margin = 8
        self.func = lambda: True

    def is_hover(self, pos):
        hover_x = self.rect.x < pos[0] < self.rect.x + self.rect.width
        hover_y = self.rect.y < pos[1] < self.rect.y + self.rect.height

        return hover_x and hover_y

    def hover(self):
        self.color = HOVER_COLOR
        # if pg.mouse.get_cursor() != pg.SYSTEM_CURSOR_HAND:
        #     pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)

    def not_hover(self):
        self.color = BASE_COLOR
        # if pg.mouse.get_cursor() != pg.SYSTEM_CURSOR_ARROW:
        #    pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)

    def set_margin(self, margin):
        self.margin = margin
        return self

    def click(self):
        self.func()

    def on_click(self, func):
        self.func = func

    def display(self, screen):
        pg.draw.rect(screen, self.color, self.rect)
        utils.draw_text(self.text, screen, (self.rect.x + self.margin, self.rect.y + self.margin), TEXT_COLOR)
