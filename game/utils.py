import pygame as pg

TEXT_COLOR = pg.Color(255, 255, 255)
FONT_SIZE = 42

def draw_text(text, screen, pos, color=TEXT_COLOR, size=FONT_SIZE):
    font = pg.font.Font(None, size)
    text_surface = font.render(text, True, color, None)  # -> Surface

    text_rect = text_surface.get_rect(topleft=pos)  # -> Rect
    screen.blit(text_surface, text_rect)



class MyRange:
    '''
    iterable which automatically call its iterator after reach out all element
    '''
    def __init__(self, num_1, num_2):
        if num_1 <= num_2:
            self.start = num_1
            self.end = num_2
        else:
            self.start = num_2
            self.end = num_1
        


    def __iter__(self): return self.MyRange_Iterator(self)

    class MyRange_Iterator:
        '''
        iterator for myRange iterable
        '''
        def __init__(self, my_range):
            self.__index = my_range.start
            self.__my_range = my_range


        def __iter__(self): return self


        def __next__(self):
            if self.__index > self.__my_range.end:
                raise StopIteration
            
            self.__index += 1

            return self.__index - 1


for row in MyRange(9, 8):
    for col in MyRange(0, 1):
        print('row', row, 'col', col)
        
            



        


