import os
import pygame as pg

from game.setting import IMAGE_PATH
from class_types.tile_types import TileTypes
from class_types.road_types import RoadTypes
from class_types.buildind_types import BuildingTypes


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

            # Road texture
            RoadTypes.ALONE: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land2a_00104.png'))).convert_alpha(screen),
            RoadTypes.TL_ALONE: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land2a_00104.png'))).convert_alpha(screen),
            RoadTypes.TR_ALONE: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land2a_00101.png'))).convert_alpha(screen),
            RoadTypes.BR_ALONE: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land2a_00102.png'))).convert_alpha(screen),
            RoadTypes.BL_ALONE: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land2a_00103.png'))).convert_alpha(screen),
            RoadTypes.TL_TO_BR: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land2a_00096.png'))).convert_alpha(screen),
            RoadTypes.TR_TO_BL: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land2a_00095.png'))).convert_alpha(screen),
            RoadTypes.TL_TO_TR: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land2a_00100.png'))).convert_alpha(screen),
            RoadTypes.TR_TO_BR: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land2a_00097.png'))).convert_alpha(screen),
            RoadTypes.BR_TO_BL: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land2a_00098.png'))).convert_alpha(screen),
            RoadTypes.BL_TO_TL: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land2a_00099.png'))).convert_alpha(screen),
            RoadTypes.TL_TO_TR_TO_BR: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land2a_00109.png'))).convert_alpha(screen),
            RoadTypes.TR_TO_BR_TO_BL: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land2a_00106.png'))).convert_alpha(screen),
            RoadTypes.BR_TO_BL_TO_TL: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land2a_00107.png'))).convert_alpha(screen),
            RoadTypes.BL_TO_TL_TO_TR: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land2a_00108.png'))).convert_alpha(screen),
            RoadTypes.ALL_DIRECTION: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land2a_00110.png'))).convert_alpha(screen),

            # Buildings texture
            BuildingTypes.BUILD_SIGN: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Housng1a_00045.png'))).convert_alpha(screen)
        }
