import pygame as pg

from components.button import Button
from events.key_listener import KeyListener

from components.component import Component


class EventManager:
    def __init__(self):
        # Components are IU elements like button, that have different states and actions depending on the input
        # of the system. For example, a button changes its color and the cursor when its hovered
        self.components: list[Component] = []

        # Key listeners are functions that are called when the matching key is pressed
        self.key_listeners: list[KeyListener] = []

        # Mouse listeners are functions that are called at every loop of the game, without any condition
        self.mouse_listeners = []

        # Hooked functions are functions that are called with the "event" parameter as their first, and
        # any other parameters passed to them
        self.hooked_functions = []

        # The any_input function is called when any key or mouse button is pressed (excluding scroll)
        # Useful for things like "press any to continue"
        self.any_input = lambda: True


    def handle_events(self):
        """
        The logic function that has to be called in the game loop for the magic to append
        :return: The EventManager itself
        """

        pos = pg.mouse.get_pos()

        for mouse_listener in self.mouse_listeners:
            mouse_listener()

        for component in self.components:
            if component.is_hover(pos):
                component.hover()
            else:
                component.not_hover()

        for key_listener in self.key_listeners:
            if key_listener.is_being_pressed():
                key_listener.call()

        for event in pg.event.get():
            for hooked_function in self.hooked_functions:
                hooked_function[0](event, *hooked_function[1])

            if event.type == pg.KEYDOWN:
                self.any_input()
                for key_listener in self.key_listeners:
                    if key_listener.key == event.key:
                        key_listener.set_being_pressed(True)
                        key_listener.call()

            if event.type == pg.KEYUP:
                for key_listener in self.key_listeners:
                    if key_listener.key == event.key:
                        key_listener.set_being_pressed(False)

            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                for component in self.components:
                    if isinstance(component, Button) and component.is_hover(pos):
                        component.set_being_pressed(True)

            if event.type == pg.MOUSEBUTTONUP:
                # Désactive le scroll de la souris pour les click
                if event.button not in (4, 5):
                    self.any_input()
                    for component in self.components:
                        if isinstance(component, Button):
                            if component.is_hover(pos) and component.is_being_pressed():
                                if component.is_selected():
                                    component.set_selected(False)
                                else:
                                    component.set_selected(True)
                                    component.click()
                                component.set_being_pressed(False)
                            else:
                                component.set_selected(False)
                                component.set_being_pressed(False)
                        else:
                            if component.is_hover(pos):
                                component.click()
        return self

    def register_component(self, component: Component):
        """
        Add a new component to the EventManager

        Components are IU elements like button, that have different states and actions depending on the input of the system.
        For example, a button changes its color and the cursor when its hovered.

        :param component: The component to add to the EventManager
        :return: The EventManager itself
        """

        self.components.append(component)
        return self

    def remove_component(self, component: Component):
        """
        Remove an existing component from the EventManager.

        :param component: The component to remove
        :return: The EventManager itself
        """

        try:
            self.components.remove(component)
        except ValueError:
            pass
        return self


    def clear_components(self):
        """
        Remove every component from the EventManager.

        :return: The EventManager itself
        """
        self.components = []
        return self

    def register_key_listener(self, key, func, continuous_press: bool = False):
        """
        Add a new key listener to the event manager, and remove the old one bound to the key if it exists.

        Key listeners are functions that are called when the matching key is pressed.

        :param continuous_press: Call the function when the key is kept pressed
        :param key: The key associated with the function
        :param func: The function to call when the key is pressed
        :return: The EventManager itself
        """
        kl = KeyListener(func, key, continuous_press)
        self.remove_key_listener(key)
        self.key_listeners.append(kl)
        # self.key_listeners.append((key, func, continuous_press))
        return self

    def remove_key_listener(self, key):
        """
        Remove a listener associated with a specific key.

        :param key: The key associated with the listener
        :return: The EventManager itself
        """

        for listeners in self.key_listeners:
            if listeners.key == key:
                self.key_listeners.remove(listeners)
        return self

    def clear_key_listeners(self):
        """
        Remove every key listeners from the EventManager.

        :return: The EventManager itself
        """

        self.key_listeners = []
        return self

    def set_any_input(self, func):
        """
        Sets the any_input function.

        The any_input function is called when any key or mouse button is pressed (excluding scroll).
        Useful for things like "press any key to continue".

        :param func: The function to run
        :return: The EventManager itself
        """

        self.any_input = func
        return self

    def clear_any_input(self):
        """
        Remove the function to run to any input.

        :return: The EventManager itself
        """

        self.any_input = lambda: True
        return self

    def register_mouse_listener(self, func):
        """
        Add a mouse listener to the Event Manager.

        Mouse listeners are functions that are called at every loop of the game, without any condition.
        Useful to handle mouse movements, but can be used for other things.

        :param func: The function to run
        :return: The EventManager itself
        """

        self.mouse_listeners.append(func)
        return self

    def remove_mouse_listener(self, func):
        """
        Remove a specific mouse listener from the EventManager.

        :param func: The mouse listener to remove
        :return: The EventManager itself
        """

        try:
            self.mouse_listeners.remove(func)
        except ValueError:
            pass
        return self

    def clear_mouse_listeners(self):
        """
        Remove every mouse listener from the EventManager.

        :return: The EventManager itself
        """

        self.mouse_listeners = []
        return self

    def add_hooked_function(self, func, *params):
        """
        Add a hooked function to the EventManager.

        Hooked functions are functions that are called at every game loop with the "event" parameter as their first, and any other parameters passed to them.

        :param func: The function to call
        :param params: List of every parameter to call the function with (in addition to the event)
        :return: The EventManager itself
        """
        self.hooked_functions.append((func, params))
        return self

    def remove_hooked_function(self, func):
        """
        Remove a specific hook from the EventManager.

        :param func: The hook to remove
        :return: The EventManager itself
        """
        for hooked_fonction in self.hooked_functions:
            if hooked_fonction[0] == func:
                self.hooked_functions.remove(hooked_fonction)
        return self

    def clear_hooked_functions(self):
        """
        Remove every hook from the EventManager.

        :return: The EventManager itself
        """
        self.hooked_functions = []
        return self
