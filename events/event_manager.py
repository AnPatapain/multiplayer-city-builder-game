import json

import pygame as pg

from components.button import Button
from components.component import Component
from components.text_input import TextInput
from events.key_listener import KeyListener
from game.builder import Builder
from network_system.system_layer.read_write import SystemInterface

from class_types.network_commands_types import NetworkCommandsTypes

class EventManager:
    # Components are IU elements like button, that have different states and actions depending on the input
    # of the system. For example, a button changes its color and the cursor when its hovered
    components: list[Component] = []

    menu_deroulant = []
    # Key listeners are functions that are called when the matching key is pressed
    key_listeners: list[KeyListener] = []

    # Mouse listeners are functions that are called at every loop of the game, without any condition
    mouse_listeners = []

    # Hooked functions are functions that are called with the "event" parameter as their first, and
    # any other parameters passed to them
    hooked_functions = []

    # The any_input function is called when any key or mouse button is pressed (excluding scroll)
    # Useful for things like "press any to continue"
    any_input = lambda: True

    @staticmethod
    def handle_events():
        """
        The logic function that has to be called in the game loop for the magic to append
        :return: The EventManager itself
        """

        si = SystemInterface.get_instance()

        res = si.read_message()
        if res:
            if res["header"]["command"] == NetworkCommandsTypes.BUILD:
                d = res["data"][0]
                d = json.loads(d)
                b = Builder()
                b.build_from_start_to_end(d["building_type"], d["start"], d["end"], from_network=True)

            if res["header"]["command"] == NetworkCommandsTypes.ASK_SAVE:
                si.send_game_save()

        pos = pg.mouse.get_pos()

        for mouse_listener in EventManager.mouse_listeners:
            mouse_listener()

        for component in EventManager.components:
            if component.is_hover(pos):
                component.hover()
            else:
                component.not_hover()

        for key_listener in EventManager.key_listeners:
            if key_listener.is_being_pressed():
                key_listener.call()

        for event in pg.event.get():
            for hooked_function in EventManager.hooked_functions:
                hooked_function[0](event, *hooked_function[1])

            if event.type == pg.TEXTINPUT:
                key_pressed = False
                for component in EventManager.components:
                    if isinstance(component, TextInput) and component.is_focused():
                        component.add_character(event.text)
                        key_pressed = True
                if key_pressed:
                    continue

            if event.type == pg.KEYDOWN:
                EventManager.any_input()
                key_pressed = False
                for component in EventManager.components:
                    if isinstance(component, TextInput) and component.is_focused():
                        match event.key:
                            case pg.K_BACKSPACE:
                                component.delete_character_left()
                                key_pressed = True
                            case pg.K_DELETE:
                                component.delete_character_right()
                                key_pressed = True
                            case pg.K_LEFT:
                                component.go_left()
                                key_pressed = True
                            case pg.K_RIGHT:
                                component.go_right()
                                key_pressed = True
                            case pg.K_ESCAPE:
                                component.unfocus()
                                key_pressed = True
                if key_pressed:
                    continue

                for key_listener in EventManager.key_listeners:
                    if key_listener.key == event.key:
                        key_listener.set_being_pressed(True)
                        key_listener.call()

            if event.type == pg.KEYUP:
                for key_listener in EventManager.key_listeners:
                    if key_listener.key == event.key:
                        key_listener.set_being_pressed(False)

            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                for component in EventManager.components:
                    if isinstance(component, Button) and component.is_hover(pos):
                        component.set_being_pressed(True)
                    if isinstance(component, Button) and not component.is_hover(pos):
                        component.sous_menu_printing = False
                for sous_menu in EventManager.menu_deroulant:
                    if sous_menu.get_isActive() and not sous_menu.rectangle.collidepoint(pos):
                        sous_menu.set_isActive()


            if event.type == pg.MOUSEBUTTONUP:
                # Désactive le scroll de la souris pour les click
                if event.button not in (4, 5):
                    EventManager.any_input()
                    for component in EventManager.components:
                        if isinstance(component, Button):
                            if component.is_hover(pos) and component.is_being_pressed():
                                if component.is_selected() and not component.is_unselect_disabled():
                                    component.set_selected(False)
                                else:
                                    component.set_selected(True)
                                    for button in EventManager.components:
                                        if button.position != component.position:
                                            button.selected = False
                                    component.click()
                                component.set_being_pressed(False)
                            else:
                                if not component.is_unselect_disabled():
                                    component.set_selected(False)
                                component.set_being_pressed(False)
                        elif isinstance(component, TextInput):
                            if component.is_hover(pos):
                                component.focus()
                            else:
                                component.unfocus()
                        else:
                            if component.is_hover(pos):
                                component.click()

    @staticmethod
    def register_component(component: Component):
        """
        Add a new component to the EventManager

        Components are IU elements like button, that have different states and actions depending on the input of the system.
        For example, a button changes its color and the cursor when its hovered.

        :param component: The component to add to the EventManager
        """

        EventManager.components.append(component)

    @staticmethod
    def register_menu_deroulant(sous_menu):
        EventManager.menu_deroulant.append(sous_menu)


    @staticmethod
    def remove_component(component: Component):
        """
        Remove an existing component from the EventManager.

        :param component: The component to remove
        :return: The EventManager itself
        """

        try:
            EventManager.components.remove(component)
        except ValueError:
            pass

    @staticmethod
    def clear_components():
        """
        Remove every component from the EventManager.

        :return: The EventManager itself
        """
        EventManager.components = []

    @staticmethod
    def register_key_listener(key, func, continuous_press: bool = False):
        """
        Add a new key listener to the event manager, and remove the old one bound to the key if it exists.

        Key listeners are functions that are called when the matching key is pressed.

        :param continuous_press: Call the function when the key is kept pressed
        :param key: The key associated with the function
        :param func: The function to call when the key is pressed
        :return: The EventManager itself
        """
        kl = KeyListener(func, key, continuous_press)
        EventManager.remove_key_listener(key)
        EventManager.key_listeners.append(kl)

    @staticmethod
    def remove_key_listener(key):
        """
        Remove a listener associated with a specific key.

        :param key: The key associated with the listener
        :return: The EventManager itself
        """

        for listeners in EventManager.key_listeners:
            if listeners.key == key:
                EventManager.key_listeners.remove(listeners)

    @staticmethod
    def clear_key_listeners():
        """
        Remove every key listeners from the EventManager.

        :return: The EventManager itself
        """

        EventManager.key_listeners = []

    @staticmethod
    def set_any_input(func):
        """
        Sets the any_input function.

        The any_input function is called when any key or mouse button is pressed (excluding scroll).
        Useful for things like "press any key to continue".

        :param func: The function to run
        :return: The EventManager itself
        """

        EventManager.any_input = func

    @staticmethod
    def clear_any_input():
        """
        Remove the function to run to any input.

        :return: The EventManager itself
        """

        EventManager.any_input = lambda: True

    @staticmethod
    def register_mouse_listener(func):
        """
        Add a mouse listener to the Event Manager.

        Mouse listeners are functions that are called at every loop of the game, without any condition.
        Useful to handle mouse movements, but can be used for other things.

        :param func: The function to run
        :return: The EventManager itself
        """

        EventManager.mouse_listeners.append(func)

    @staticmethod
    def remove_mouse_listener(func):
        """
        Remove a specific mouse listener from the EventManager.

        :param func: The mouse listener to remove
        :return: The EventManager itself
        """

        try:
            EventManager.mouse_listeners.remove(func)
        except ValueError:
            pass

    @staticmethod
    def clear_mouse_listeners():
        """
        Remove every mouse listener from the EventManager.

        :return: The EventManager itself
        """

        EventManager.mouse_listeners = []

    @staticmethod
    def add_hooked_function(func, *params):
        """
        Add a hooked function to the EventManager.

        Hooked functions are functions that are called at every game loop with the "event" parameter as their first, and any other parameters passed to them.

        :param func: The function to call
        :param params: List of every parameter to call the function with (in addition to the event)
        :return: The EventManager itself
        """
        EventManager.hooked_functions.append((func, params))

    @staticmethod
    def remove_hooked_function(func):
        """
        Remove a specific hook from the EventManager.

        :param func: The hook to remove
        :return: The EventManager itself
        """
        for hooked_fonction in EventManager.hooked_functions:
            if hooked_fonction[0] == func:
                EventManager.hooked_functions.remove(hooked_fonction)

    @staticmethod
    def clear_hooked_functions():
        """
        Remove every hook from the EventManager.

        :return: The EventManager itself
        """
        EventManager.hooked_functions = []

    @staticmethod
    def reset():
        EventManager.clear_components()
        EventManager.clear_hooked_functions()
        EventManager.clear_any_input()
        EventManager.clear_key_listeners()
        EventManager.clear_mouse_listeners()
