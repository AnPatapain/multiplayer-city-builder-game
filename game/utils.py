import pygame as pg

def draw_text(text, size, screen, pos):
    font = pg.font.Font(None, size)
    text_surface = font.render(text, True, (0,0, 0), None) # -> Surface
    

    text_rect = text_surface.get_rect(topleft=pos) # -> Rect 
    screen.blit(text_surface, text_rect)