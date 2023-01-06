import pygame as pg

from pygame import Surface, Rect, Color
from components.component import Component
from game import utils

TEXT_COLOR = Color(27, 27, 27)

BASE_COLOR = Color(154, 146, 121)
HOVER_COLOR = Color(139, 131, 106)
SELECTED_COLOR = Color(139, 131, 106)
DISABLED_COLOR = Color(120, 120, 90)

class Button(Component):
    def __init__(
            self,
            pos,
            size,
            text: str = "",
            image: Surface = None,
            image_hover: Surface = None,
            image_selected: Surface = None,
            center_text: bool = False,
            selectable: bool = False,
    ):
        super().__init__(pos, size)
        self.text = text
        self.bg_color = BASE_COLOR
        self.bg = Rect(self.position, self.size)
        self.margin = 8
        self.text_centered = center_text
        self.selectable = selectable
        self.selected = False
        self.being_pressed = False
        self.disabled = False
        self.image = image
        self.image_selected = image_selected
        self.image_hover = image_hover

    def is_hover(self, pos):
        return self.bg.collidepoint(pos)

    def hover(self):
        if not self.is_hovered() and not self.is_disabled():
            self.bg_color = HOVER_COLOR
            if pg.mouse.get_cursor() != pg.SYSTEM_CURSOR_HAND:
                pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
            self.hovered = True

    def not_hover(self):
        if self.is_hovered() and not self.is_disabled():
            self.bg_color = BASE_COLOR
            if pg.mouse.get_cursor() != pg.SYSTEM_CURSOR_ARROW:
                pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)
            self.hovered = False

    def set_margin(self, margin: int):
        self.margin = margin
        return self

    def is_selected(self):
        return self.selected

    def set_selected(self, status: bool):
        if not self.is_disabled() and self.selectable:
            self.selected = status

    def is_being_pressed(self):
        return self.being_pressed

    def set_being_pressed(self, being_pressed: bool):
        if not self.is_disabled():
            self.being_pressed = being_pressed

    def is_disabled(self):
        return self.disabled

    def set_disabled(self, disabled: bool):
        self.disabled = disabled

    def click(self):
        if not self.is_disabled():
            if not self.selectable:
                self.not_hover()
            super().click()

    def display(self, screen: Surface):
        color = BASE_COLOR
        if self.is_disabled():
            color = DISABLED_COLOR
        elif self.is_selected():
            color = SELECTED_COLOR
        elif self.is_hovered():
            color = HOVER_COLOR
        elif self.is_being_pressed():
            color = HOVER_COLOR

        pg.draw.rect(screen, color, self.bg)
        center = None

        pos = (self.bg.x + self.margin, self.bg.y + self.margin)
        if self.text_centered:
            pos = (self.bg.x, self.bg.y + self.margin)
            center = self.size[0]

        if (self.is_hovered() or self.is_being_pressed()) and self.image_hover is not None:
            screen.blit(self.image_hover, self.bg)
        elif self.is_selected() and self.image_selected is not None:
            screen.blit(self.image_selected, self.bg)
        elif self.image is not None:
            screen.blit(self.image, self.bg)

        utils.draw_text(self.text, screen, pos, TEXT_COLOR, center_on_width=center)
