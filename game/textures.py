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
    textures: dict[pg.Surface] = {}
    walker_textures: dict[WalkerTypes, dict[OrientationTypes, dict[int, pg.Surface]]] = {}
    textures_destroy: dict[pg.Surface] = {}

    @staticmethod
    def get_texture(texture_id: any) -> pg.Surface | dict[Enum, pg.Surface]:
        return Textures.textures[texture_id]

    @staticmethod
    def get_walker_texture(walker_id: WalkerTypes, direction: OrientationTypes, animation_frame: int) -> pg.Surface:
        return Textures.walker_textures[walker_id][direction][animation_frame]

    @staticmethod
    def get_delete_texture(texture_id: any) -> pg.Surface:
        texture = Textures.textures_destroy.get(texture_id)
        if texture is None:
            new_texture = Textures.get_texture(texture_id).copy()
            Textures.fill(new_texture)
            Textures.textures_destroy[texture_id] = new_texture
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


            TileTypes.ROCK: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00290.png'))).convert_alpha(screen),
            TileTypes.TREE: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00041.png'))).convert_alpha(screen),
            TileTypes.BIG_TREE: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00059.png'))).convert_alpha(screen),
            TileTypes.WATER: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00120.png'))).convert_alpha(screen),
            TileTypes.WHEAT: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Land1a_00027.png'))).convert_alpha(screen),

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
            BuildingTypes.SMALL_TENT: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Housng1a_00001.png'))).convert_alpha(screen),
            BuildingTypes.LARGE_TENT: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Housng1a_00004.png'))).convert_alpha(screen),
            BuildingTypes.SMALL_SHACK: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Housng1a_00007.png'))).convert_alpha(screen),
            BuildingTypes.LARGE_SHACK: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Housng1a_00009.png'))).convert_alpha(screen),
            BuildingTypes.BUILD_SIGN: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Housng1a_00045.png'))).convert_alpha(screen),
            BuildingTypes.PREFECTURE: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Security_00001.png'))).convert_alpha(screen),
            BuildingTypes.PELLE: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'destroy_design.png'))).convert_alpha(screen),
            BuildingTypes.WELL: pg.transform.scale2x(pg.image.load(os.path.join(IMAGE_PATH, 'Utilitya_00001.png'))).convert_alpha(screen),

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
                    1: pg.image.load(os.path.join(IMAGE_PATH, 'Citizen01_01047.png')).convert_alpha(screen)
                },
                OrientationTypes.TOP_RIGHT: {
                    1: pg.image.load(os.path.join(IMAGE_PATH, 'Citizen01_01033.png')).convert_alpha(screen)
                },
                OrientationTypes.BOTTOM_RIGHT: {
                    1: pg.image.load(os.path.join(IMAGE_PATH, 'Citizen01_01083.png')).convert_alpha(screen)
                },
                OrientationTypes.BOTTOM_LEFT: {
                    1: pg.image.load(os.path.join(IMAGE_PATH, 'Citizen01_01061.png')).convert_alpha(screen)
                },
            },
            WalkerTypes.PREFET: {
                OrientationTypes.TOP_LEFT: {
                    1: pg.image.load(os.path.join(IMAGE_PATH, 'citizen02_00661.png')).convert_alpha(screen)
                },
                OrientationTypes.TOP_RIGHT: {
                    1: pg.image.load(os.path.join(IMAGE_PATH, 'citizen02_00623.png')).convert_alpha(screen)
                },
                OrientationTypes.BOTTOM_RIGHT: {
                    1: pg.image.load(os.path.join(IMAGE_PATH, 'citizen02_00657.png')).convert_alpha(screen)
                },
                OrientationTypes.BOTTOM_LEFT: {
                    1: pg.image.load(os.path.join(IMAGE_PATH, 'citizen02_00627.png')).convert_alpha(screen)
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
