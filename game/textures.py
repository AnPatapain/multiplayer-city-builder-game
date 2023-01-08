import os
from enum import Enum

import pygame as pg

from class_types.walker_types import WalkerTypes
from game.setting import IMAGE_PATH
from class_types.tile_types import TileTypes
from class_types.road_types import RoadTypes
from class_types.buildind_types import BuildingTypes
from class_types.panel_types import SwitchViewButtonTypes
from class_types.orientation_types import OrientationTypes


class Textures:
    textures: dict[Enum, pg.Surface | dict[int, pg.Surface]] = {}
    walker_textures: dict[WalkerTypes, dict[OrientationTypes, dict[int, pg.Surface]]] = {}
    textures_destroy: dict[pg.Surface] = {}

    @staticmethod
    def get_texture(texture_id: any, texture_number: int = 0) -> pg.Surface:
        texture = Textures.textures[texture_id]
        if isinstance(texture, dict):
            if texture_number:
                try:
                    return texture[texture_number]
                except KeyError:
                    return texture[0]
            else:
                return texture[0]
        else:
            return texture

    @staticmethod
    def get_walker_texture(walker_id: WalkerTypes, direction: OrientationTypes, animation_frame: int) -> pg.Surface:
        animation_frame = animation_frame % len(Textures.walker_textures[walker_id][direction])
        return Textures.walker_textures[walker_id][direction][animation_frame]

    @staticmethod
    def get_delete_texture(texture_id: any, texture_number: int = 0) -> pg.Surface:
        texture = Textures.textures_destroy.get(texture_id)
        if texture:
            texture = texture.get(texture_number)
        if texture is None:
            new_texture = Textures.get_texture(texture_id, texture_number).copy()
            Textures.fill(new_texture)
            if Textures.textures_destroy.get(texture_id) is None:
                Textures.textures_destroy[texture_id] = {}
            Textures.textures_destroy[texture_id] |= {texture_number: new_texture}
            texture = new_texture
        return texture

    @staticmethod
    def init(screen):
        Textures.textures = {
            TileTypes.GRASS: {
                0: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00232.png'))).convert_alpha(screen),
                1: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00233.png'))).convert_alpha(screen),
                2: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00265.png'))).convert_alpha(screen),
                3: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00235.png'))).convert_alpha(screen),
                4: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00236.png'))).convert_alpha(screen),
                5: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00257.png'))).convert_alpha(screen),
                6: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00238.png'))).convert_alpha(screen),
                7: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00239.png'))).convert_alpha(screen),
                8: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00240.png'))).convert_alpha(
                    screen),
                9: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00241.png'))).convert_alpha(
                    screen),
                10: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00242.png'))).convert_alpha(
                    screen),
                11: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00243.png'))).convert_alpha(
                    screen),
                12: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00244.png'))).convert_alpha(
                    screen),
                13: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00245.png'))).convert_alpha(
                    screen),
                14: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00246.png'))).convert_alpha(
                    screen),
                15: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00247.png'))).convert_alpha(
                    screen),
                16: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00248.png'))).convert_alpha(
                    screen),
                17: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00249.png'))).convert_alpha(
                    screen),
                18: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00250.png'))).convert_alpha(
                    screen),
                19: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00251.png'))).convert_alpha(
                    screen),
                20: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00252.png'))).convert_alpha(
                    screen),

            },

            TileTypes.ROCK: {
                0: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'land3a_00071.png'))).convert_alpha(screen),
                1: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'land3a_00078.png'))).convert_alpha(screen),
                2: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'land3a_00072.png'))).convert_alpha(
                    screen),
                3: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'land3a_00073.png'))).convert_alpha(
                    screen),
                4: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'land3a_00074.png'))).convert_alpha(
                    screen),
                5: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'land3a_00075.png'))).convert_alpha(
                    screen),
                6: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'land3a_00076.png'))).convert_alpha(
                    screen),
                7: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'land3a_00077.png'))).convert_alpha(
                    screen),
                20: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'land3a_00079.png'))).convert_alpha(
                    screen),
                21: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'land3a_00080.png'))).convert_alpha(
                    screen),
                22: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'land3a_00081.png'))).convert_alpha(
                    screen),
                23: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'land3a_00082.png'))).convert_alpha(
                    screen),
                30: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'land3a_00083.png'))).convert_alpha(
                    screen),
                31: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'land3a_00084.png'))).convert_alpha(
                    screen)
            },

            TileTypes.TREE: {
                0: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00010.png'))).convert_alpha(screen),
                1: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00011.png'))).convert_alpha(screen),
                2: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00012.png'))).convert_alpha(
                    screen),
                3: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00013.png'))).convert_alpha(
                    screen),
                4: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00014.png'))).convert_alpha(
                    screen),
                5: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00015.png'))).convert_alpha(
                    screen),
                6: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00016.png'))).convert_alpha(
                    screen),
                7: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00017.png'))).convert_alpha(
                    screen),
                8: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00030.png'))).convert_alpha(
                    screen),
                9: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00031.png'))).convert_alpha(
                    screen),
                10: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00032.png'))).convert_alpha(
                    screen),
                11: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00033.png'))).convert_alpha(
                    screen),
                12: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00034.png'))).convert_alpha(
                    screen),
                13: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00035.png'))).convert_alpha(
                    screen),
                14: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00036.png'))).convert_alpha(
                    screen),
                15: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00037.png'))).convert_alpha(
                    screen),
                16: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00038.png'))).convert_alpha(
                    screen),
                17: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00039.png'))).convert_alpha(
                    screen),
                18: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00040.png'))).convert_alpha(
                    screen),
                19: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00041.png'))).convert_alpha(
                    screen),
                20: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00042.png'))).convert_alpha(
                    screen),
                21: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00043.png'))).convert_alpha(
                    screen),
                22: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00044.png'))).convert_alpha(
                    screen),
                23: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00045.png'))).convert_alpha(
                    screen),
                24: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00046.png'))).convert_alpha(
                    screen),
                25: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00047.png'))).convert_alpha(
                    screen),
                26: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00048.png'))).convert_alpha(
                    screen),
                27: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00049.png'))).convert_alpha(
                    screen),
                28: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00055.png'))).convert_alpha(
                    screen),
                29: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00051.png'))).convert_alpha(
                    screen),
                30: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00052.png'))).convert_alpha(
                    screen),
                31: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00053.png'))).convert_alpha(
                    screen),
                32: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00053.png'))).convert_alpha(
                    screen),
                33: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00054.png'))).convert_alpha(
                    screen),
                34: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00058.png'))).convert_alpha(
                    screen),
                35: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00059.png'))).convert_alpha(
                    screen),
                36: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00060.png'))).convert_alpha(
                    screen),
            },

            TileTypes.WATER: {
                0: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00120.png'))).convert_alpha(screen),
                1: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00121.png'))).convert_alpha(screen),
                2: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00122.png'))).convert_alpha(screen),
                3: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00123.png'))).convert_alpha(screen),
                4: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00124.png'))).convert_alpha(screen),
                5: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00125.png'))).convert_alpha(screen),
                6: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00126.png'))).convert_alpha(screen),
                7: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00127.png'))).convert_alpha(screen),
                10: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00137.png'))).convert_alpha(
                    screen),
                11: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00151.png'))).convert_alpha(
                    screen),
                12: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00152.png'))).convert_alpha(
                    screen),
                13: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00153.png'))).convert_alpha(
                    screen),
                14: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00132.png'))).convert_alpha(
                    screen),
                15: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00147.png'))).convert_alpha(
                    screen),
                16: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00145.png'))).convert_alpha(
                    screen),
                17: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00128.png'))).convert_alpha(
                    screen),
                18: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00146.png'))).convert_alpha(
                    screen),
                19: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00159.png'))).convert_alpha(
                    screen),
                20: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00144.png'))).convert_alpha(
                    screen),
                21: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00140.png'))).convert_alpha(
                    screen),
                22: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00154.png'))).convert_alpha(
                    screen),
                23: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00156.png'))).convert_alpha(
                    screen),
                24: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00155.png'))).convert_alpha(
                    screen),
                70: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00170.png'))).convert_alpha(
                    screen),
                71: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00173.png'))).convert_alpha(
                    screen),
                72: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00171.png'))).convert_alpha(
                    screen),
                73: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00172.png'))).convert_alpha(
                    screen),
            },

            TileTypes.WHEAT: {
                0: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00027.png'))).convert_alpha(screen),
                1: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00028.png'))).convert_alpha(screen),
                2: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00029.png'))).convert_alpha(
                    screen),
                3: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00026.png'))).convert_alpha(
                    screen),
                10: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00021.png'))).convert_alpha(
                    screen),
                11: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00020.png'))).convert_alpha(
                    screen),
                12: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00019.png'))).convert_alpha(
                    screen),
                13: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00018.png'))).convert_alpha(
                    screen),
                20: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00022.png'))).convert_alpha(
                    screen),
                21: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00023.png'))).convert_alpha(
                    screen),
                22: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00024.png'))).convert_alpha(
                    screen),
                23: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00025.png'))).convert_alpha(
                    screen),
            },

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

            #
            # Buildings texture
            BuildingTypes.VACANT_HOUSE: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Housng1a_00045.png'))).convert_alpha(screen),
            BuildingTypes.SMALL_TENT: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Housng1a_00001.png'))).convert_alpha(screen),
            BuildingTypes.LARGE_TENT: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Housng1a_00004.png'))).convert_alpha(screen),
            BuildingTypes.SMALL_SHACK: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Housng1a_00007.png'))).convert_alpha(screen),
            BuildingTypes.LARGE_SHACK: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Housng1a_00009.png'))).convert_alpha(screen),
            BuildingTypes.BUILD_SIGN: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Housng1a_00045.png'))).convert_alpha(screen),
            BuildingTypes.PREFECTURE: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Security_00001.png'))).convert_alpha(screen),
            BuildingTypes.PELLE: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'destroy_design.png'))).convert_alpha(screen),
            BuildingTypes.WELL: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Utilitya_00001.png'))).convert_alpha(screen),
            BuildingTypes.WHEAT_FARM: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Commerce_00012.png'))).convert_alpha(screen),
            BuildingTypes.EMPTY_WHEAT_SOL: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Commerce_00013.png'))).convert_alpha(screen),
            BuildingTypes.FULL_WHEAT_SOL: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Commerce_00017.png'))).convert_alpha(screen),

            # Panel icon texture
            # BuildingButtonTypes.ROAD: pg.image.load(os.path.join(IMAGE_PATH, '')).convert_alpha(screen),

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
            SwitchViewButtonTypes.BUTTON5_HOVER: pg.image.load(os.path.join(IMAGE_PATH, 'paneling_00124.png')).convert_alpha(screen),
            SwitchViewButtonTypes.BUTTON5_SELECTED: pg.image.load(os.path.join(IMAGE_PATH, 'paneling_00125.png')).convert_alpha(screen),
            SwitchViewButtonTypes.BUTTON6: pg.image.load(os.path.join(IMAGE_PATH, 'paneling_00131.png')).convert_alpha(screen),
            SwitchViewButtonTypes.BUTTON6_HOVER: pg.image.load(os.path.join(IMAGE_PATH, 'paneling_00132.png')).convert_alpha(screen),
            SwitchViewButtonTypes.BUTTON6_SELECTED: pg.image.load(os.path.join(IMAGE_PATH, 'paneling_00133.png')).convert_alpha(screen),
            SwitchViewButtonTypes.BUTTON7: pg.image.load(os.path.join(IMAGE_PATH, 'paneling_00135.png')).convert_alpha(screen),
            SwitchViewButtonTypes.BUTTON7_HOVER: pg.image.load(os.path.join(IMAGE_PATH, 'paneling_00136.png')).convert_alpha(screen),
            SwitchViewButtonTypes.BUTTON7_SELECTED: pg.image.load(os.path.join(IMAGE_PATH, 'paneling_00137.png')).convert_alpha(screen),
            SwitchViewButtonTypes.BUTTON8: pg.image.load(os.path.join(IMAGE_PATH, 'paneling_00127.png')).convert_alpha(screen),
            SwitchViewButtonTypes.BUTTON8_HOVER: pg.image.load(os.path.join(IMAGE_PATH, 'paneling_00128.png')).convert_alpha(screen),
            SwitchViewButtonTypes.BUTTON8_SELECTED: pg.image.load(os.path.join(IMAGE_PATH, 'paneling_00129.png')).convert_alpha(screen),
            SwitchViewButtonTypes.BUTTON9: pg.image.load(os.path.join(IMAGE_PATH, 'paneling_00163.png')).convert_alpha(screen),
            SwitchViewButtonTypes.BUTTON10: pg.image.load(os.path.join(IMAGE_PATH, 'paneling_00151.png')).convert_alpha(screen),
            SwitchViewButtonTypes.BUTTON11: pg.image.load(os.path.join(IMAGE_PATH, 'paneling_00147.png')).convert_alpha(screen),
            SwitchViewButtonTypes.BUTTON12: pg.image.load(os.path.join(IMAGE_PATH, 'paneling_00143.png')).convert_alpha(screen),
            SwitchViewButtonTypes.BUTTON13: pg.image.load(os.path.join(IMAGE_PATH, 'paneling_00139.png')).convert_alpha(screen),
            SwitchViewButtonTypes.BUTTON14: pg.image.load(os.path.join(IMAGE_PATH, 'paneling_00167.png')).convert_alpha(screen),
            SwitchViewButtonTypes.BUTTON15: pg.image.load(os.path.join(IMAGE_PATH, 'paneling_00159.png')).convert_alpha(screen),
            SwitchViewButtonTypes.BUTTON15_HOVER: pg.image.load(os.path.join(IMAGE_PATH, 'paneling_00160.png')).convert_alpha(screen),
            SwitchViewButtonTypes.BUTTON15_SELECTED: pg.image.load(os.path.join(IMAGE_PATH, 'paneling_00161.png')).convert_alpha(screen),
            SwitchViewButtonTypes.BUTTON16: pg.image.load(os.path.join(IMAGE_PATH, 'paneling_00155.png')).convert_alpha(screen),
            SwitchViewButtonTypes.BUTTON17: pg.image.load(os.path.join(IMAGE_PATH, 'paneling_00171.png')).convert_alpha(screen),
            SwitchViewButtonTypes.BUTTON18: pg.image.load(os.path.join(IMAGE_PATH, 'paneling_00115.png')).convert_alpha(screen),
            SwitchViewButtonTypes.BUTTON19: pg.image.load(os.path.join(IMAGE_PATH, 'paneling_00119.png')).convert_alpha(screen),
            SwitchViewButtonTypes.BOTTOM_PANNEL: pg.image.load(os.path.join(IMAGE_PATH, 'fenetre.png')).convert_alpha(screen),
        }

        Textures.walker_textures = {
            WalkerTypes.MIGRANT: {
                OrientationTypes.TOP_LEFT: {
                    0: pg.image.load(os.path.join(IMAGE_PATH, 'Citizen01_01039.png')).convert_alpha(screen),
                    1: pg.image.load(os.path.join(IMAGE_PATH, 'Citizen01_01047.png')).convert_alpha(screen),
                    2: pg.image.load(os.path.join(IMAGE_PATH, 'Citizen01_01055.png')).convert_alpha(screen),
                    3: pg.image.load(os.path.join(IMAGE_PATH, 'Citizen01_01063.png')).convert_alpha(screen),
                    4: pg.image.load(os.path.join(IMAGE_PATH, 'Citizen01_01071.png')).convert_alpha(screen),
                    5: pg.image.load(os.path.join(IMAGE_PATH, 'Citizen01_01079.png')).convert_alpha(screen),
                    6: pg.image.load(os.path.join(IMAGE_PATH, 'Citizen01_01087.png')).convert_alpha(screen),
                    7: pg.image.load(os.path.join(IMAGE_PATH, 'Citizen01_01095.png')).convert_alpha(screen),
                    8: pg.image.load(os.path.join(IMAGE_PATH, 'Citizen01_01103.png')).convert_alpha(screen),
                    9: pg.image.load(os.path.join(IMAGE_PATH, 'Citizen01_01111.png')).convert_alpha(screen),
                    10: pg.image.load(os.path.join(IMAGE_PATH, 'Citizen01_01119.png')).convert_alpha(screen),
                    11: pg.image.load(os.path.join(IMAGE_PATH, 'Citizen01_01127.png')).convert_alpha(screen),
                },
                OrientationTypes.TOP_RIGHT: {
                    0: pg.image.load(os.path.join(IMAGE_PATH, 'Citizen01_01033.png')).convert_alpha(screen),
                    1: pg.image.load(os.path.join(IMAGE_PATH, 'Citizen01_01041.png')).convert_alpha(screen),
                    2: pg.image.load(os.path.join(IMAGE_PATH, 'Citizen01_01049.png')).convert_alpha(screen),
                    3: pg.image.load(os.path.join(IMAGE_PATH, 'Citizen01_01057.png')).convert_alpha(screen),
                    4: pg.image.load(os.path.join(IMAGE_PATH, 'Citizen01_01065.png')).convert_alpha(screen),
                    5: pg.image.load(os.path.join(IMAGE_PATH, 'Citizen01_01073.png')).convert_alpha(screen),
                    6: pg.image.load(os.path.join(IMAGE_PATH, 'Citizen01_01081.png')).convert_alpha(screen),
                    7: pg.image.load(os.path.join(IMAGE_PATH, 'Citizen01_01089.png')).convert_alpha(screen),
                    8: pg.image.load(os.path.join(IMAGE_PATH, 'Citizen01_01097.png')).convert_alpha(screen),
                    9: pg.image.load(os.path.join(IMAGE_PATH, 'Citizen01_01105.png')).convert_alpha(screen),
                    10: pg.image.load(os.path.join(IMAGE_PATH, 'Citizen01_01113.png')).convert_alpha(screen),
                    11: pg.image.load(os.path.join(IMAGE_PATH, 'Citizen01_01121.png')).convert_alpha(screen),
                },
                OrientationTypes.BOTTOM_RIGHT: {
                    0: pg.image.load(os.path.join(IMAGE_PATH, 'Citizen01_01035.png')).convert_alpha(screen),
                    1: pg.image.load(os.path.join(IMAGE_PATH, 'Citizen01_01043.png')).convert_alpha(screen),
                    2: pg.image.load(os.path.join(IMAGE_PATH, 'Citizen01_01051.png')).convert_alpha(screen),
                    3: pg.image.load(os.path.join(IMAGE_PATH, 'Citizen01_01059.png')).convert_alpha(screen),
                    4: pg.image.load(os.path.join(IMAGE_PATH, 'Citizen01_01067.png')).convert_alpha(screen),
                    5: pg.image.load(os.path.join(IMAGE_PATH, 'Citizen01_01075.png')).convert_alpha(screen),
                    6: pg.image.load(os.path.join(IMAGE_PATH, 'Citizen01_01083.png')).convert_alpha(screen),
                    7: pg.image.load(os.path.join(IMAGE_PATH, 'Citizen01_01091.png')).convert_alpha(screen),
                    8: pg.image.load(os.path.join(IMAGE_PATH, 'Citizen01_01099.png')).convert_alpha(screen),
                    9: pg.image.load(os.path.join(IMAGE_PATH, 'Citizen01_01107.png')).convert_alpha(screen),
                    10: pg.image.load(os.path.join(IMAGE_PATH, 'Citizen01_01115.png')).convert_alpha(screen),
                    11: pg.image.load(os.path.join(IMAGE_PATH, 'Citizen01_01123.png')).convert_alpha(screen),
                },
                OrientationTypes.BOTTOM_LEFT: {
                    0: pg.image.load(os.path.join(IMAGE_PATH, 'Citizen01_01037.png')).convert_alpha(screen),
                    1: pg.image.load(os.path.join(IMAGE_PATH, 'Citizen01_01045.png')).convert_alpha(screen),
                    2: pg.image.load(os.path.join(IMAGE_PATH, 'Citizen01_01053.png')).convert_alpha(screen),
                    3: pg.image.load(os.path.join(IMAGE_PATH, 'Citizen01_01061.png')).convert_alpha(screen),
                    4: pg.image.load(os.path.join(IMAGE_PATH, 'Citizen01_01069.png')).convert_alpha(screen),
                    5: pg.image.load(os.path.join(IMAGE_PATH, 'Citizen01_01077.png')).convert_alpha(screen),
                    6: pg.image.load(os.path.join(IMAGE_PATH, 'Citizen01_01085.png')).convert_alpha(screen),
                    7: pg.image.load(os.path.join(IMAGE_PATH, 'Citizen01_01093.png')).convert_alpha(screen),
                    8: pg.image.load(os.path.join(IMAGE_PATH, 'Citizen01_01101.png')).convert_alpha(screen),
                    9: pg.image.load(os.path.join(IMAGE_PATH, 'Citizen01_01109.png')).convert_alpha(screen),
                    10: pg.image.load(os.path.join(IMAGE_PATH, 'Citizen01_01117.png')).convert_alpha(screen),
                    11: pg.image.load(os.path.join(IMAGE_PATH, 'Citizen01_01125.png')).convert_alpha(screen),
                },
            },
            WalkerTypes.PREFET: {
                OrientationTypes.TOP_LEFT: {
                    0: pg.image.load(os.path.join(IMAGE_PATH, 'citizen02_00621.png')).convert_alpha(screen),
                    1: pg.image.load(os.path.join(IMAGE_PATH, 'citizen02_00629.png')).convert_alpha(screen),
                    2: pg.image.load(os.path.join(IMAGE_PATH, 'citizen02_00637.png')).convert_alpha(screen),
                    3: pg.image.load(os.path.join(IMAGE_PATH, 'citizen02_00645.png')).convert_alpha(screen),
                    4: pg.image.load(os.path.join(IMAGE_PATH, 'citizen02_00653.png')).convert_alpha(screen),
                    5: pg.image.load(os.path.join(IMAGE_PATH, 'citizen02_00661.png')).convert_alpha(screen),
                    6: pg.image.load(os.path.join(IMAGE_PATH, 'citizen02_00669.png')).convert_alpha(screen),
                    7: pg.image.load(os.path.join(IMAGE_PATH, 'citizen02_00677.png')).convert_alpha(screen),
                    8: pg.image.load(os.path.join(IMAGE_PATH, 'citizen02_00685.png')).convert_alpha(screen),
                    9: pg.image.load(os.path.join(IMAGE_PATH, 'citizen02_00693.png')).convert_alpha(screen),
                    10: pg.image.load(os.path.join(IMAGE_PATH, 'citizen02_00701.png')).convert_alpha(screen),
                    11: pg.image.load(os.path.join(IMAGE_PATH, 'citizen02_00709.png')).convert_alpha(screen),
                },
                OrientationTypes.TOP_RIGHT: {
                    0: pg.image.load(os.path.join(IMAGE_PATH, 'citizen02_00623.png')).convert_alpha(screen),
                    1: pg.image.load(os.path.join(IMAGE_PATH, 'citizen02_00631.png')).convert_alpha(screen),
                    2: pg.image.load(os.path.join(IMAGE_PATH, 'citizen02_00639.png')).convert_alpha(screen),
                    3: pg.image.load(os.path.join(IMAGE_PATH, 'citizen02_00647.png')).convert_alpha(screen),
                    4: pg.image.load(os.path.join(IMAGE_PATH, 'citizen02_00655.png')).convert_alpha(screen),
                    5: pg.image.load(os.path.join(IMAGE_PATH, 'citizen02_00663.png')).convert_alpha(screen),
                    6: pg.image.load(os.path.join(IMAGE_PATH, 'citizen02_00671.png')).convert_alpha(screen),
                    7: pg.image.load(os.path.join(IMAGE_PATH, 'citizen02_00679.png')).convert_alpha(screen),
                    8: pg.image.load(os.path.join(IMAGE_PATH, 'citizen02_00687.png')).convert_alpha(screen),
                    9: pg.image.load(os.path.join(IMAGE_PATH, 'citizen02_00695.png')).convert_alpha(screen),
                    10: pg.image.load(os.path.join(IMAGE_PATH, 'citizen02_00703.png')).convert_alpha(screen),
                    11: pg.image.load(os.path.join(IMAGE_PATH, 'citizen02_00615.png')).convert_alpha(screen),
                },
                OrientationTypes.BOTTOM_RIGHT: {
                    0: pg.image.load(os.path.join(IMAGE_PATH, 'citizen02_00617.png')).convert_alpha(screen),
                    1: pg.image.load(os.path.join(IMAGE_PATH, 'citizen02_00625.png')).convert_alpha(screen),
                    2: pg.image.load(os.path.join(IMAGE_PATH, 'citizen02_00633.png')).convert_alpha(screen),
                    3: pg.image.load(os.path.join(IMAGE_PATH, 'citizen02_00641.png')).convert_alpha(screen),
                    4: pg.image.load(os.path.join(IMAGE_PATH, 'citizen02_00649.png')).convert_alpha(screen),
                    5: pg.image.load(os.path.join(IMAGE_PATH, 'citizen02_00657.png')).convert_alpha(screen),
                    6: pg.image.load(os.path.join(IMAGE_PATH, 'citizen02_00665.png')).convert_alpha(screen),
                    7: pg.image.load(os.path.join(IMAGE_PATH, 'citizen02_00673.png')).convert_alpha(screen),
                    8: pg.image.load(os.path.join(IMAGE_PATH, 'citizen02_00681.png')).convert_alpha(screen),
                    9: pg.image.load(os.path.join(IMAGE_PATH, 'citizen02_00689.png')).convert_alpha(screen),
                    10: pg.image.load(os.path.join(IMAGE_PATH, 'citizen02_00697.png')).convert_alpha(screen),
                    11: pg.image.load(os.path.join(IMAGE_PATH, 'citizen02_00697.png')).convert_alpha(screen),
                },
                OrientationTypes.BOTTOM_LEFT: {
                    0: pg.image.load(os.path.join(IMAGE_PATH, 'citizen02_00619.png')).convert_alpha(screen),
                    1: pg.image.load(os.path.join(IMAGE_PATH, 'citizen02_00627.png')).convert_alpha(screen),
                    2: pg.image.load(os.path.join(IMAGE_PATH, 'citizen02_00635.png')).convert_alpha(screen),
                    3: pg.image.load(os.path.join(IMAGE_PATH, 'citizen02_00643.png')).convert_alpha(screen),
                    4: pg.image.load(os.path.join(IMAGE_PATH, 'citizen02_00651.png')).convert_alpha(screen),
                    5: pg.image.load(os.path.join(IMAGE_PATH, 'citizen02_00659.png')).convert_alpha(screen),
                    6: pg.image.load(os.path.join(IMAGE_PATH, 'citizen02_00667.png')).convert_alpha(screen),
                    7: pg.image.load(os.path.join(IMAGE_PATH, 'citizen02_00675.png')).convert_alpha(screen),
                    8: pg.image.load(os.path.join(IMAGE_PATH, 'citizen02_00683.png')).convert_alpha(screen),
                    9: pg.image.load(os.path.join(IMAGE_PATH, 'citizen02_00691.png')).convert_alpha(screen),
                    10: pg.image.load(os.path.join(IMAGE_PATH, 'citizen02_00699.png')).convert_alpha(screen),
                    11: pg.image.load(os.path.join(IMAGE_PATH, 'citizen02_00707.png')).convert_alpha(screen),
                },
            }
        }


    @staticmethod
    def fill(surface):
        """Fill all pixels of the surface with color, preserve transparency."""
        w, h = surface.get_size()
        for x in range(w):
            for y in range(h):
                r, g, b, a = surface.get_at((x, y))
                if a == 255:
                    surface.set_at((x, y), pg.Color(150, 0, 24, 100))
                if r >= 5:
                    surface.set_at((x, y), pg.Color(r, 0, 24, 100))
