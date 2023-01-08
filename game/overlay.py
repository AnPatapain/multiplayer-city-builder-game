import os
from enum import Enum

import pygame
from PIL import Image

from buildable.buildable import Buildable
from buildable.house import House
from buildable.structure import Structure
from class_types.overlay_types import OverlayTypes
from game.setting import IMAGE_PATH, GRID_SIZE
from map_element.tile import Tile


class OverlaySprite(Enum):
    HOLE = 1

    BASE = 2
    CAPITAL = 3
    COLUMN_PART = 4

    YELLOW_BASE = 12
    YELLOW_CAPITAL = 13
    YELLOW_COLUMN_PART = 14

    ORANGE_BASE = 22
    ORANGE_CAPITAL = 23
    ORANGE_COLUMN_PART = 24

    RED_BASE = 32
    RED_CAPITAL = 33
    RED_COLUMN_PART = 34


class Overlay:
    instance = None
    def __init__(self):
        self.pg_image_fire_overlay = [ [None]*GRID_SIZE for i in range(GRID_SIZE)]
        self.pg_image_dest_overlay = [ [None]*GRID_SIZE for i in range(GRID_SIZE)]
        self.overlay_types = OverlayTypes.DEFAULT

        self.sprite = {
            OverlaySprite.HOLE : Image.open(os.path.join(IMAGE_PATH, 'Land2a_00001.png')),

            OverlaySprite.BASE : Image.open(os.path.join(IMAGE_PATH, 'Sprites_00011.png')),
            OverlaySprite.COLUMN_PART : Image.open(os.path.join(IMAGE_PATH, 'Sprites_00010.png')),
            OverlaySprite.CAPITAL : Image.open(os.path.join(IMAGE_PATH, 'Sprites_00009.png')),

            OverlaySprite.YELLOW_BASE: Image.open(os.path.join(IMAGE_PATH, 'Sprites_00014.png')),
            OverlaySprite.YELLOW_COLUMN_PART: Image.open(os.path.join(IMAGE_PATH, 'Sprites_00013.png')),
            OverlaySprite.YELLOW_CAPITAL: Image.open(os.path.join(IMAGE_PATH, 'Sprites_00012.png')),

            OverlaySprite.ORANGE_BASE: Image.open(os.path.join(IMAGE_PATH, 'Sprites_00017.png')),
            OverlaySprite.ORANGE_COLUMN_PART: Image.open(os.path.join(IMAGE_PATH, 'Sprites_00016.png')),
            OverlaySprite.ORANGE_CAPITAL: Image.open(os.path.join(IMAGE_PATH, 'Sprites_00015.png')),

            OverlaySprite.RED_BASE: Image.open(os.path.join(IMAGE_PATH, 'Sprites_00020.png')),
            OverlaySprite.RED_COLUMN_PART: Image.open(os.path.join(IMAGE_PATH, 'Sprites_00019.png')),
            OverlaySprite.RED_CAPITAL: Image.open(os.path.join(IMAGE_PATH, 'Sprites_00018.png')),

        }


    def get_overlay(self,tile : Tile) -> pygame.image:
        building = tile.get_building()
        if isinstance(building,House) or isinstance(building,Structure):
            #Image update
            match self.overlay_types:
                case OverlayTypes.FIRE:
                    if not self.pg_image_fire_overlay[tile.x][tile.y] or building.get_risk().is_update():
                        self.pg_image_fire_overlay[tile.x][tile.y] = self.update_overlay(building)

                    return self.pg_image_fire_overlay[tile.x][tile.y]

                case OverlayTypes.DESTRUCTION:
                    if not self.pg_image_dest_overlay[tile.x][tile.y] or building.get_risk().is_update():
                        self.pg_image_dest_overlay[tile.x][tile.y] = self.update_overlay(building)

                    return self.pg_image_dest_overlay[tile.x][tile.y]

                case _:
                    print("Bad Overlay")
                    return None
        return None

    def update_overlay(self,building : Buildable) -> pygame.image:
        if not building.get_risk():
            return None

        level = 0
        match self.overlay_types:
            case OverlayTypes.FIRE:
                level = building.get_risk().get_fire_status()
            case OverlayTypes.DESTRUCTION:
                level = building.get_risk().get_dest_status()

        if level == -1:
            return None
        else:
            level = int(level / 10)

        building.get_risk().updated()

        if level <= 0:
            return self.to_pg_imgage(self.sprite[OverlaySprite.HOLE])

        if 1 <= level < 2:
            new_image = self.init_image(38)
            new_image.paste(self.sprite[OverlaySprite.BASE], (9, new_image.height - self.sprite[OverlaySprite.BASE].height - 4))
            return self.to_pg_imgage(new_image)

        if 2 <= level < 3:
            new_image = self.init_image(58)
            new_image.paste(self.sprite[OverlaySprite.BASE],(9,new_image.height - self.sprite[OverlaySprite.BASE].height - 4))
            new_image.paste(self.sprite[OverlaySprite.CAPITAL],(5,new_image.height - self.sprite[OverlaySprite.CAPITAL].height - 4 - 21))
            return self.to_pg_imgage(new_image)

        if 3 <= level <= 10:
            column_part_th = level - 2
            new_image = self.init_image(58 + 9 * column_part_th)

            #CLASSIC
            if 3 <= level < 4:
                new_image.paste(self.sprite[OverlaySprite.BASE],(9,new_image.height - self.sprite[OverlaySprite.BASE].height - 4))
                new_image.paste(self.sprite[OverlaySprite.COLUMN_PART],(17,new_image.height - self.sprite[OverlaySprite.COLUMN_PART].height - 4 - 21))
                new_image.paste(self.sprite[OverlaySprite.CAPITAL],(5,new_image.height - self.sprite[OverlaySprite.CAPITAL].height - 4 - 21 - 9 * column_part_th))

            #YELLOW
            elif 4 <= level < 7:
                new_image.paste(self.sprite[OverlaySprite.YELLOW_BASE],(9, new_image.height - self.sprite[OverlaySprite.YELLOW_BASE].height - 4))

                for i in range(column_part_th):
                    new_image.paste(self.sprite[OverlaySprite.YELLOW_COLUMN_PART], (17, new_image.height - self.sprite[OverlaySprite.YELLOW_COLUMN_PART].height - 4 - 21 - i * 9))

                new_image.paste(self.sprite[OverlaySprite.YELLOW_CAPITAL],(5, new_image.height - self.sprite[OverlaySprite.YELLOW_CAPITAL].height - 4 - 21 - 9 * column_part_th))

            #ORANGE
            elif 7 <= level < 9:
                new_image.paste(self.sprite[OverlaySprite.ORANGE_BASE],(9, new_image.height - self.sprite[OverlaySprite.ORANGE_BASE].height - 4))
                for i in range(level):
                    new_image.paste(self.sprite[OverlaySprite.ORANGE_COLUMN_PART], (17, new_image.height - self.sprite[OverlaySprite.ORANGE_COLUMN_PART].height - 4 - 21 - i * 9))

                new_image.paste(self.sprite[OverlaySprite.ORANGE_CAPITAL],(5, new_image.height - self.sprite[OverlaySprite.ORANGE_CAPITAL].height - 4 - 21 - 9 * column_part_th))
            #RED
            elif 9 <= level <= 10:
                new_image.paste(self.sprite[OverlaySprite.RED_BASE],(9, new_image.height - self.sprite[OverlaySprite.RED_BASE].height - 4))

                for i in range(level):
                    new_image.paste(self.sprite[OverlaySprite.RED_COLUMN_PART], (17, new_image.height - self.sprite[OverlaySprite.RED_COLUMN_PART].height - 4 - 21 - i * 9))

                new_image.paste(self.sprite[OverlaySprite.RED_CAPITAL],(5, new_image.height - self.sprite[OverlaySprite.RED_CAPITAL].height - 4 - 21 - 9 * column_part_th))

            return self.to_pg_imgage(new_image)

        return None

    def to_pg_imgage(self,image : Image) -> pygame.image:
        return pygame.transform.scale2x(pygame.image.fromstring(image.tobytes(), image.size, image.mode))

    def init_image(self,height) -> Image:
        image = Image.new("RGBA", size=(self.sprite[OverlaySprite.HOLE].width,height), color=(0, 0, 0, 0))
        image.paste(self.sprite[OverlaySprite.HOLE], (0, image.height - self.sprite[OverlaySprite.HOLE].height))
        return image

    def set_overlay_types(self):
        match self.overlay_types:
            case OverlayTypes.FIRE:
                self.overlay_types = OverlayTypes.DESTRUCTION
            case OverlayTypes.DESTRUCTION:
                self.overlay_types = OverlayTypes.DEFAULT
            case OverlayTypes.DEFAULT:
                self.overlay_types = OverlayTypes.FIRE

    def get_overlay_types(self):
        return self.overlay_types

    def get_name(self):
        match self.overlay_types:
            case OverlayTypes.DEFAULT:
                return "Default"
            case OverlayTypes.FIRE:
                return "Fire"
            case OverlayTypes.DESTRUCTION:
                return "Damage"

        return "Overlay"

    @staticmethod
    def get_instance():
        if Overlay.instance is None:
            Overlay.instance = Overlay()
        return Overlay.instance