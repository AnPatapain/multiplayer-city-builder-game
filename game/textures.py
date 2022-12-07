import os
import pygame as pg

from game.setting import IMAGE_PATH
from class_types.tile_types import TileTypes
from class_types.panel_types import BuildingButtonTypes, SwitchViewButtonTypes


class Textures:
    textures: dict[pg.Surface] = {}

    @staticmethod
    def get_texture(texture_id: any) -> pg.Surface:
        return Textures.textures[texture_id]

    @staticmethod
    def init(screen):
        Textures.textures = {
            TileTypes.GRASS: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00069.png'))).convert_alpha(screen),
            TileTypes.ROCK: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00290.png'))).convert_alpha(screen),
            TileTypes.TREE: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00041.png'))).convert_alpha(screen),

            #BuildingButtonTypes.ROAD: pg.image.load(os.path.join(IMAGE_PATH, '')).convert_alpha(screen),

            SwitchViewButtonTypes.SCULPTURE: pg.image.load(os.path.join(IMAGE_PATH, 'paneling_00018.png')).convert_alpha(screen),
            SwitchViewButtonTypes.MINI_SCULPTURE: pg.image.load(os.path.join(IMAGE_PATH, 'panelwindows_00013.png')).convert_alpha(screen),
            SwitchViewButtonTypes.TOP_PANNEL: pg.image.load(os.path.join(IMAGE_PATH, 'paneling_00017.png')).convert_alpha(screen),
            SwitchViewButtonTypes.DYNAMIC_DISPLAY: pg.image.load(os.path.join(IMAGE_PATH, 'paneling_00015.png')).convert_alpha(screen),
            SwitchViewButtonTypes.BARRE: pg.image.load(os.path.join(IMAGE_PATH, 'barre.png')).convert_alpha(screen),
            SwitchViewButtonTypes.JULIUS: pg.image.load(os.path.join(IMAGE_PATH, 'paneling_00079.png')).convert_alpha(screen),
            SwitchViewButtonTypes.EUROPEAN: pg.image.load(os.path.join(IMAGE_PATH, 'paneling_00082.png')).convert_alpha(screen),

            SwitchViewButtonTypes.BUTTON1: pg.image.load(os.path.join(IMAGE_PATH, 'paneling_00085.png')).convert_alpha(screen),
            SwitchViewButtonTypes.BUTTON2: pg.image.load(os.path.join(IMAGE_PATH, 'paneling_00088.png')).convert_alpha(screen),
            SwitchViewButtonTypes.BUTTON3: pg.image.load(os.path.join(IMAGE_PATH, 'paneling_00091.png')).convert_alpha(screen),
            SwitchViewButtonTypes.BUTTON4: pg.image.load(os.path.join(IMAGE_PATH, 'paneling_00094.png')).convert_alpha(screen),

            SwitchViewButtonTypes.BUTTON5: pg.image.load(os.path.join(IMAGE_PATH, 'paneling_00123.png')).convert_alpha(screen),
            SwitchViewButtonTypes.BUTTON6: pg.image.load(os.path.join(IMAGE_PATH, 'paneling_00131.png')).convert_alpha(screen),
            SwitchViewButtonTypes.BUTTON7: pg.image.load(os.path.join(IMAGE_PATH, 'paneling_00135.png')).convert_alpha(screen),
            SwitchViewButtonTypes.BUTTON8: pg.image.load(os.path.join(IMAGE_PATH, 'paneling_00127.png')).convert_alpha(screen),
            SwitchViewButtonTypes.BUTTON9: pg.image.load(os.path.join(IMAGE_PATH, 'paneling_00163.png')).convert_alpha(screen),
            SwitchViewButtonTypes.BUTTON10: pg.image.load(os.path.join(IMAGE_PATH, 'paneling_00151.png')).convert_alpha(screen),
            SwitchViewButtonTypes.BUTTON11: pg.image.load(os.path.join(IMAGE_PATH, 'paneling_00147.png')).convert_alpha(screen),
            SwitchViewButtonTypes.BUTTON12: pg.image.load(os.path.join(IMAGE_PATH, 'paneling_00143.png')).convert_alpha(screen),
            SwitchViewButtonTypes.BUTTON13: pg.image.load(os.path.join(IMAGE_PATH, 'paneling_00139.png')).convert_alpha(screen),
            SwitchViewButtonTypes.BUTTON14: pg.image.load(os.path.join(IMAGE_PATH, 'paneling_00167.png')).convert_alpha(screen),
            SwitchViewButtonTypes.BUTTON15: pg.image.load(os.path.join(IMAGE_PATH, 'paneling_00159.png')).convert_alpha(screen),
            SwitchViewButtonTypes.BUTTON16: pg.image.load(os.path.join(IMAGE_PATH, 'paneling_00155.png')).convert_alpha(screen),
            SwitchViewButtonTypes.BUTTON17: pg.image.load(os.path.join(IMAGE_PATH, 'paneling_00171.png')).convert_alpha(screen),
            SwitchViewButtonTypes.BUTTON18: pg.image.load(os.path.join(IMAGE_PATH, 'paneling_00115.png')).convert_alpha(screen),
            SwitchViewButtonTypes.BUTTON19: pg.image.load(os.path.join(IMAGE_PATH, 'paneling_00119.png')).convert_alpha(screen),
            SwitchViewButtonTypes.BOTTOM_PANNEL: pg.image.load(os.path.join(IMAGE_PATH, 'fenetre.png')).convert_alpha(screen),

        }

