import pygame as pg

class SoundManager:

    def __init__(self):
        pg.mixer.init()
        self.sounds = {
            'menu_demarrer': pg.mixer.Sound("sounds/mp3/Rome4.mp3"),
            'debut_jeu': pg.mixer.Sound('sounds/mp3/Rome1.mp3')
        }

    def play(self, name):
        # I comment it because i don't want my beautiful jazz playlist suspended :  )
        self.sounds[name].play()

    def stop(self, name):
        self.sounds[name].stop()
