import pygame as pg

TEXT_COLOR = pg.Color(255, 255, 255)
FONT_SIZE = 42

def draw_text(text, screen, pos, color=TEXT_COLOR):
    font = pg.font.Font(None, FONT_SIZE)
    text_surface = font.render(text, True, color, None)  # -> Surface

    text_rect = text_surface.get_rect(topleft=pos)  # -> Rect
    screen.blit(text_surface, text_rect)
