import pygame as pg

from components.component import Component
from game import utils

TEXT_COLOR = pg.Color(27, 27, 27)
BASE_COLOR = pg.Color(154, 146, 121)
HOVER_COLOR = pg.Color(139, 131, 106)

class Button(Component):
    def __init__(self, text, pos, size, center: bool = False, image=None):
        super().__init__(pos, size)
        self.text = text
        self.bg_color = BASE_COLOR
        self.bg = pg.Rect(self.position, self.size)
        self.margin = 8
        self.text_centered = center
        self.image = image
        self.image_hovered = image
        if self.image_hovered is not None:
            self.image_hovered.set_alpha(200)

    def is_hover(self, pos):
        return self.bg.collidepoint(pos)

    def hover(self):
        if not self.is_hovered:
            self.bg_color = HOVER_COLOR
            if pg.mouse.get_cursor() != pg.SYSTEM_CURSOR_HAND:
                pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
            self.is_hovered = True

    def not_hover(self):
        if self.is_hovered:
            self.bg_color = BASE_COLOR
            if pg.mouse.get_cursor() != pg.SYSTEM_CURSOR_ARROW:
                pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)
            self.is_hovered = False

    def set_margin(self, margin):
        self.margin = margin
        return self

    def click(self):
        self.not_hover()
        super().click()

    def display(self, screen):
        pg.draw.rect(screen, self.bg_color, self.bg)
        center = None

        if self.image is not None:
            if self.is_hovered:
                screen.blit(self.image_hovered, self.bg)
            else:
                screen.blit(self.image, self.bg)
            return

        pos = (self.bg.x + self.margin, self.bg.y + self.margin)
        if self.text_centered:
            pos = (self.bg.x, self.bg.y + self.margin)
            center = self.size[0]

        utils.draw_text(self.text, screen, pos, TEXT_COLOR, center_on_width=center)

