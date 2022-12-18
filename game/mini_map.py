import pygame as pg


class MiniMap:
    def __init__(self) -> None:
        self.mini_screen_width = 48
        self.mini_screen_height = 27

        self.mm_width = 145
        self.mm_height = 111

        self.background = pg.Surface((self.mm_width, self.mm_height))
        self.background.fill((0, 0, 0))
        pg.draw.polygon(self.background, (0, 255, 0),
                        [(self.mm_width / 2, 0),
                         (self.mm_width, self.mm_height / 2),
                         (self.mm_width / 2, self.mm_height),
                         (0, self.mm_height / 2)], 1)

        self.camera_zone_rect = None

        # self.pos_x = width - self.mm_width - 8
        self.pos_x = 1920 - self.mm_width - 8
        self.pos_y = 81  # 46 = topbar height

    def draw(self, screen, map_pos):
        # We need coordination of 4 points to draw rhombus
        self.camera_zone_rect = pg.Rect(- map_pos[0] * 0.024,
                                        - map_pos[1] * 0.037,
                                        self.mini_screen_width, self.mini_screen_height)

        temp_bg = self.background.copy()
        pg.draw.rect(temp_bg, (255, 255, 0), self.camera_zone_rect, 1)
        screen.blit(temp_bg, (self.pos_x, self.pos_y))
