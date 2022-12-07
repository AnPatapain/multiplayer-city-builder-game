import pygame as pg

class SoundManager:

    def __init__(self):
        pg.mixer.init(44100, -16, 2, 2048)
        self.sounds = {
            'menu_demarrer': pg.mixer.Sound("sounds/mp3/Rome4.wav"),
            #'debut_jeu': pg.mixer.Sound('sounds/mp3/Rome1.mp3'),
        }

    def play(self, name):
        self.sounds[name].play()
