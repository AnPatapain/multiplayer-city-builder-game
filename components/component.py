from abc import abstractmethod

from pygame import Surface

class Component:
    def __init__(self, position: tuple[int, int], size: tuple[int, int]):
        self.position = position
        self.size = size
        self.on_click_func = lambda: None
        self.is_hovered = False

    def is_hover(self, pos):
        hover_x = self.position[0] < pos[0] < self.position[0] + self.size[0]
        hover_y = self.position[1] < pos[1] < self.position[1] + self.size[1]

        return hover_x and hover_y

    @abstractmethod
    def hover(self):
        pass

    @abstractmethod
    def not_hover(self):
        pass

    def on_click(self, func):
        self.on_click_func = func

    def click(self):
        self.on_click_func()

    @abstractmethod
    def display(self, screen: Surface):
        pass
