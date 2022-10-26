import pygame as pg


class EventManager:
    def __init__(self):
        self.components = []
        self.key_listeners = []
        self.any_input = lambda: True

    def handle_events(self):
        pos = pg.mouse.get_pos()

        for component in self.components:
            if component.is_hover(pos):
                component.hover()
            else:
                component.not_hover()

        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                self.any_input()
                for key_listener in self.key_listeners:
                    if key_listener[0] == event.key:
                        key_listener[1]()

            if event.type == pg.MOUSEBUTTONUP:
                # Désactive le scroll de la souris pour les click
                if event.button not in (4, 5):
                    self.any_input()
                    for component in self.components:
                        if component.is_hover(pos):
                            component.click()

    def register_component(self, component):
        self.components.append(component)
        return self

    def remove_component(self, component):
        try:
            self.components.remove(component)
        except ValueError:
            pass
        return self

    def clear_components(self):
        self.components = []
        return self

    def register_key_listener(self, key, func):
        # Retire le listener existant si conflit avec une touche
        self.remove_component(key)
        self.key_listeners.append((key, func))
        return self

    def remove_key_listener(self, key):
        for listeners in self.key_listeners:
            if listeners[0] == key:
                self.key_listeners.remove(listeners)
        return self

    def clear_key_listener(self):
        self.key_listeners = []
        return self

    def set_any_input(self, func):
        self.any_input = func
        return self

    def clear_any_input(self):
        self.any_input = lambda: True
