from class_types.tile_types import TileTypes
from game.textures import Textures
from game.setting import TILE_SIZE


class Tile:
    def __init__(self, col: int, row: int, tile_type: TileTypes = TileTypes.GRASS):
        self.type = tile_type
        self.building = None
        self.road = None

        cartesian_coord = [
            (col * TILE_SIZE, row * TILE_SIZE),
            (col * TILE_SIZE + TILE_SIZE, row * TILE_SIZE),
            (col * TILE_SIZE + TILE_SIZE, row * TILE_SIZE + TILE_SIZE),
            (col * TILE_SIZE, row * TILE_SIZE + TILE_SIZE)
        ]

        def convert_cartesian_to_isometric(x, y):
            return x - y, (x + y) / 2

        self.isometric_coord = [convert_cartesian_to_isometric(x, y) for x, y in cartesian_coord]
        self.render_coord = (
            min([x for x, y in self.isometric_coord]),
            min([y for x, y in self.isometric_coord])
        )

    def get_render_coord(self):
        return self.render_coord

    def get_isometric_coord(self):
        return self.isometric_coord

    def get_type(self):
        return self.type

    def set_type(self, new_type):
        self.type = new_type

    def get_building(self):
        return self.building

    def set_building(self, new_building):
        self.building = new_building

    def get_road(self):
        return self.road

    def set_road(self,new_road):
        self.road = new_road
        self.type = self.road.get_road_type()

    def get_texture(self):
        if self.road:
            return Textures.get_texture(self.road.get_road_type())
        # TODO: get texture of building if it exists
        return Textures.get_texture(self.type)

    def get_delete_texture(self):
        if self.road:
            return Textures.get_delete_texture(self.road.get_road_type())
        # TODO: get texture of building if it exists
        return Textures.get_delete_texture(self.type)

    def is_buildable(self):
        return self.building is None \
               and self.road is None \
               and self.type in (TileTypes.WHEAT, TileTypes.GRASS)

    def is_destroyable(self):
        if self.type in (TileTypes.WHEAT, TileTypes.GRASS) : return False
        else : return True

    def destroy(self):
        self.road = None # Brute force self road to None
        self.building = None # Brute force self building to None
        self.type = TileTypes.GRASS
