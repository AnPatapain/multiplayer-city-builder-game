import pygame as pg

def draw_text(text, screen, pos):
    font = pg.font.Font(None, 42)
    text_surface = font.render(text, True, (255,255, 255), None) # -> Surface
    

    text_rect = text_surface.get_rect(topleft=pos) # -> Rect 
    screen.blit(text_surface, text_rect)