import time
from typing import TYPE_CHECKING

import pygame as pg
from pygame import Rect

if TYPE_CHECKING:
    from pygame import Surface

from components.component import Component
from game.utils import draw_text


class TextInput(Component):
    def __init__(
            self,
            pos: tuple[int, int],
            size: tuple[int, int],
            placeholder: str
    ):
        super().__init__(pos, size)
        self.current_value = ""
        self.position = pos
        self.size = size
        self.bg = Rect(self.position, self.size)
        self.placeholder = placeholder
        self.cursor_position = 0
        self.focused = True

    def focus(self):
        self.focused = True
        # Allow repeating key, useful when longpressing delete key
        pg.key.set_repeat(500, 40)

    def unfocus(self):
        self.focused = False
        # Remove key repeat, to not interfer with custom implementation used to move camera
        pg.key.set_repeat()

    def is_focused(self) -> bool:
        return self.focused

    def is_hover(self, pos):
        return (self.position[0] <= pos[0] <= self.position[0] + self.size[0]) or \
            (self.position[1] <= pos[1] <= self.position[1] + self.size[1])

    def not_hover(self):
        pass

    def click(self):
        self.focus()

    def add_character(self, char: str):
        self.current_value = self.current_value[:self.cursor_position] + char + self.current_value[
                                                                                self.cursor_position:]
        self.cursor_position += 1

    # Delete using Backspace key
    def delete_character_left(self):
        if self.cursor_position > 0:
            self.current_value = self.current_value[:self.cursor_position - 1] + self.current_value[
                                                                                 self.cursor_position:]
            self.cursor_position -= 1

    # Delete using Suppr key
    def delete_character_right(self):
        if self.cursor_position < len(self.current_value):
            self.current_value = self.current_value[:self.cursor_position] + self.current_value[self.cursor_position + 1:]

    def go_left(self):
        if self.cursor_position > 0:
            self.cursor_position -= 1

    def go_right(self):
        if self.cursor_position < len(self.current_value):
            self.cursor_position += 1

    def get_text(self):
        return self.current_value

    def clear_text(self):
        self.current_value = 0
        self.cursor_position = 0

    def display(self, screen: 'Surface'):
        pg.draw.rect(screen, (50, 50, 50), self.bg)
        draw_text(self.current_value, screen, self.position)

        # Blinks the cursor every 0.5s
        if self.is_focused() and time.time() % 1 > 0.5:
            draw_text("|", screen, (self.position[0] + self.cursor_position * 12 - 6, self.position[1]))
