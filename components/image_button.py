import pygame as pg

from components.button import Button

class ButtonImage(Button):
    def __init__(self, pos: tuple[int, int], size: tuple[int, int], image: pg.Surface):
        super().__init__("", pos, size)
        self.image = image

    def display(self, screen):
        pg.draw.rect(screen, self.bg_color, self.bg)
        screen.blit(self.image, self.bg)
