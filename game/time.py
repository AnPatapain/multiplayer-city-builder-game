from game.utils import draw_text
from .game_controller import GameController
import pygame as pg
#from game import Game

class Time:

    def __init__(self):
        self.start_time = 10000
        self.timer = 0
        self.lastime = 0

        self.months = {
            0: "Jan", 1: "Feb", 2: "Mar", 3: "Apr", 4: "May", 5: "Jun", 6: "Jul", 7: "Aug", 8: "Sep", 9: "Oct", 10: "Nov", 11: "Dec"
        }

    def get_month(self, id: int):
        return self.months[id]

    def init_timer(self):
        self.timer = (self.start_time - pg.time.get_ticks())//1000
        if self.timer == 0:
            self.update_date()

    def update_date(self):
        gc = GameController.get_instance()
        gc.increase_month()



