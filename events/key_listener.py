class KeyListener:
    def __init__(self, func, key, continuous_press: bool = False):
        self.func = func
        self.key = key
        self.continuous_press = continuous_press
        self.being_pressed = False

    def set_being_pressed(self, being_pressed: bool):
        if self.continuous_press:
            self.being_pressed = being_pressed

    def call(self):
        self.func()
