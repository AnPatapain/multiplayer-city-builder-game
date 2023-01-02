import pygame as pg
import random as rd
import string as st
from pygame.surface import Surface

TEXT_COLOR = pg.Color(255, 255, 255)
FONT_SIZE = 42

def draw_text(text: str, screen: Surface, pos: tuple[int, int], color: pg.Color = TEXT_COLOR, size: int = FONT_SIZE, center_on_width: int = None):
    font = pg.font.Font(None, size)
    text_surface = font.render(text, True, color, None)  # -> Surface

    if center_on_width:
        # Calculate the size difference between the size to center on and the size needed to render the text
        # Divide then by 2 to have the margin needed on each size (we will only use margin of the left)
        left_margin = (center_on_width - text_surface.get_width()) / 2
        if left_margin > 0:
            # We cant directly do pos[0} += left_margin, so we recreate entirely the tuple.
            pos = (pos[0] + left_margin, pos[1])

    text_rect = text_surface.get_rect(topleft=pos)  # -> Rect
    screen.blit(text_surface, text_rect)


def generate_uid(size: int = 10) -> str:
    """
    Generate a random UID composed of ASCII letters (with or without caps) and numbers.

    :param size: The length of the UID (optional, default to 10)
    :return: The UID (as a string)
    """

    return ''.join([rd.choice(st.ascii_letters + st.digits) for _ in range(size)])


class MyRange:
    """
    iterable which automatically call its iterator after reach out all element
    """
    def __init__(self, num_1, num_2):
        if num_1 <= num_2:
            self.start = num_1
            self.end = num_2
        else:
            self.start = num_2
            self.end = num_1



    def __iter__(self): return self.MyRangeIterator(self)

    class MyRangeIterator:
        """
        iterator for myRange iterable
        """
        def __init__(self, my_range):
            self.__index = my_range.start
            self.__my_range = my_range


        def __iter__(self): return self


        def __next__(self):
            if self.__index > self.__my_range.end:
                raise StopIteration

            self.__index += 1

            return self.__index - 1
