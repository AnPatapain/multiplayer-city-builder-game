from abc import abstractmethod

from pygame import Surface

class Component:
    def __init__(self, position: tuple[int, int], size: tuple[int, int]):
        self.position = position
        self.size = size
        self.on_click_func = lambda: None
        self.hovered = False

    def is_hovered(self):
        return self.hovered

    @abstractmethod
    def is_hover(self, pos):
        print("FIXME: Method is_hover not implemented!")
        pass

    @abstractmethod
    def hover(self):
        print("FIXME: Method hover not implemented!")
        pass

    @abstractmethod
    def not_hover(self):
        print("FIXME: Method not_hover not implemented!")
        pass

    def on_click(self, func):
        self.on_click_func = func

    def click(self):
        self.on_click_func()

    @abstractmethod
    def display(self, screen: Surface):
        print("FIXME: Method display not implemented!")
        pass
