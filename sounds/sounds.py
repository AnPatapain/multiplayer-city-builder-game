import pygame as pg

class SoundManager:

    def __init__(self):
        pg.mixer.init(44100, -16, 2, 2048)
        self.sounds = {
            'bouton_hover': pg.mixer.Sound("sounds/wavs/ICON1.WAV"),
            'bouton_select': pg.mixer.Sound('sounds/wavs/ARROW.WAV'),
            'ecoulement_batiment': pg.mixer.Sound('sounds/wavs/EXPLOD1.WAV'),
            'batiment_en_feu': pg.mixer.Sound('sounds/wavs/burning_ruin.wav'),
            'build_action': pg.mixer.Sound('sounds/wavs/BUILD1.WAV'),
            'fire_splash': pg.mixer.Sound('sounds/wavs/Fire_splash.wav'),

        }

    def play(self, name):
        # I comment it because i don't want my beautiful jazz playlist suspended :  )
        self.sounds[name].play()

    def stop(self, name):
        self.sounds[name].stop()
