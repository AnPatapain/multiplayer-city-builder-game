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
            text_size : int = 38,
            text: str = "",
            text_fn: () = None,
            image: Surface = None,
            image_hover: Surface = None,
            image_selected: Surface = None,
            center_text: bool = False,
            selectable: bool = False,
            disable_unselect: bool = False,
            text_pop_up: str = ""
    ):
        super().__init__(pos, size)
        self.text = text
        self.text_fn = text_fn
        self.text_size = text_size
        self.bg_color = BASE_COLOR
        self.bg = Rect(self.position, self.size)
        self.margin = 8
        self.text_centered = center_text
        self.selectable = selectable
        self.selected = False
        self.disable_unselect = disable_unselect
        self.being_pressed = False
        self.disabled = False
        self.image = image
        self.image_selected = image_selected
        self.image_hover = image_hover
        self.text_pop_up = text_pop_up
        self.surface_text_pop_up = pg.font.SysFont('default_font', 22).render(self.text_pop_up, False, (0,0,0), (255,255,255))


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

    def is_unselect_disabled(self):
        return self.disable_unselect

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
            color = SELECTED_COLOR


        pg.draw.rect(screen, color, self.bg)
        center_width = None
        center_height = None

        pos = (self.bg.x + self.margin, self.bg.y + self.margin)
        if self.text_centered:
            pos = (self.bg.x, self.bg.y + self.margin)
            center_width = self.size[0]
            center_height = self.size[1]

        if (self.is_hovered() or self.is_being_pressed()) and self.image_hover is not None:
            screen.blit(self.image_hover, self.bg)
            print(self.text_pop_up)
            if self.text_pop_up is not None:
                mouse_position = pg.mouse.get_pos()
                screen.blit(self.surface_text_pop_up, (mouse_position[0] - 100, mouse_position[1]+20))
                print(self.text_pop_up)
        elif self.is_selected() and self.image_selected is not None:
            screen.blit(self.image_selected, self.bg)
        elif self.image is not None:
            screen.blit(self.image, self.bg)

        if self.text_fn:
            self.text = self.text_fn()
        utils.draw_text(self.text, screen, pos, TEXT_COLOR, center_on_width=center_width, center_on_height=center_height, size=self.text_size)
