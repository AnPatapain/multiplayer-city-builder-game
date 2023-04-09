from abc import abstractmethod

from pygame import Surface

class Component:
    def __init__(self, position: tuple[int, int], size: tuple[int, int]):
        self.position = position
        self.size = size
        self.on_click_func = lambda: None
        self.on_click_func2 = lambda: None
        self.two_function = False
        self.hovered = False

    def is_hovered(self):
        return self.hovered

    @abstractmethod
    def is_hover(self, pos):
        print("FIXME: Method is_hover not implemented!")
        pass

    @abstractmethod
    def hover(self):
        #print("FIXM E: Method hover not implemented!")
        pass

    @abstractmethod
    def not_hover(self):
        print("FIXME: Method not_hover not implemented!")
        pass

    def on_click(self, func, func2=None):
        self.on_click_func = func
        if func2 is not None:
            self.on_click_func2 = func2
            self.two_function = True

    def on_click2(self, func2):
        self.on_click_func2 = func2
        self.two_function = True

    def click(self):
        self.on_click_func()
        if self.two_function:
            self.on_click_func2()

    @abstractmethod
    def display(self, screen: Surface):
        print("FIXME: Method display not implemented!")
        pass
