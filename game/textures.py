import os
import pygame as pg

from game.setting import IMAGE_PATH
from class_types.tile_types import TileTypes


class Textures:
    textures = {}

    @staticmethod
    def get_texture(id: any):
        return Textures.textures[id]

    @staticmethod
    def init(screen):
        Textures.textures = {
            TileTypes.GRASS: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00069.png'))).convert_alpha(screen),
            TileTypes.ROCK: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00290.png'))).convert_alpha(screen),
            TileTypes.TREE: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00041.png'))).convert_alpha(screen),
        }

