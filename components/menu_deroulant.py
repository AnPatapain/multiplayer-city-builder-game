import pygame

from components.button import Button
from events.event_manager import EventManager


class Menu_Deroulant:
    def __init__(self, button_to_scroll: Button, sous_menu_buttons : list, screen):
        self.screen = screen

        self.bouton_principal = button_to_scroll
        self.bouton_principal.on_click(lambda: self.set_isActive())

        self.sous_menu_buttons = sous_menu_buttons
        self.isActive = False
        self.taille = ()
        self.position = ()
        self.calcul_taille_position()
        self.rectangle = pygame.Rect(self.position[0], self.position[1], self.taille[0], self.taille[1])

    def get_sous_menu_buttons(self):
        return self.sous_menu_buttons

    def get_isActive(self):
        return self.isActive

    def set_isActive(self):
        self.isActive = not self.isActive
        # pos = pg.mouse.get_pos()

        for button in self.get_sous_menu_buttons():
            if self.isActive:
                EventManager.register_component(button)
            else:
                button.sous_menu_printing = False
                EventManager.remove_component(button)

    def calcul_taille_position(self):
        liste = self.get_sous_menu_buttons()
        bouton = liste[0]
        self.taille += (bouton.size[0],)
        self.taille += (len(liste) * bouton.size[1],)
        min_x, min_y = 3000, 3000
        for bouton in liste:
            if bouton.position[0] < min_x:
                min_x = bouton.position[0]
            if bouton.position[1] < min_y:
                min_y = bouton.position[1]

        self.position += (min_x,)
        self.position += (min_y,)

    def display(self):
        for button in self.get_sous_menu_buttons():
            button.display(self.screen)
