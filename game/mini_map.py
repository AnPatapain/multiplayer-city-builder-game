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

        self.mini_relative_x = None
        self.mini_relative_y = None

        # EventManager.register_mouse_listener(self.mini_map_mouse_listener)


    # def mini_map_mouse_listener(self):
    #     mouse_pos = pg.mouse.get_pos()
    #     mouse_action = pg.mouse.get_pressed()

    #     (x, y) = mouse_pos
    #     if (self.mini_map_pos_x <= x <= self.screen_width) and (self.mini_map_pos_y < y <= self.mini_map_pos_y + self.mini_default_surface_height):
    #         if mouse_action[0]:
    #             self.mini_relative_x = x - self.mini_map_pos_x
    #             self.mini_relative_y = y - self.mini_map_pos_y
    #         else:
    #             self.mini_relative_x = None
    #             self.mini_relative_y = None


    # def update(self, map_controller: MapController):
    #     if self.mini_relative_x is not None and self.mini_relative_y is not None:
    #         corresponding_x = - (self.mini_relative_x - self.mini_screen_width/2) / self.scale_down_ratio
    #         corresponding_y = - (self.mini_relative_y - self.mini_screen_height/2) / self.scale_down_ratio
    #         map_controller.set_map_pos(corresponding_x, corresponding_y)
        

    def draw(self, screen, map_pos):
        # We need coordination of 4 points to draw rhombus
        self.camera_zone_rect = pg.Rect(- map_pos[0] * 0.024,
                                        - map_pos[1] * 0.037,
                                        self.mini_screen_width, self.mini_screen_height)

        temp_bg = self.background.copy()
        pg.draw.rect(temp_bg, (255, 255, 0), self.camera_zone_rect, 1)
        screen.blit(temp_bg, (self.pos_x, self.pos_y))
