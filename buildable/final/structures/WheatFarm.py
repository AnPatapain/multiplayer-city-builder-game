from buildable.structure import Structure
from class_types.buildind_types import BuildingTypes
from map_element.tile import Tile
from game.game_controller import GameController
class WheatFarm(Structure):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, BuildingTypes.WHEAT_FARM, build_size=(3, 3), max_employee=10)
        self.game_controller = GameController.get_instance()
        self.wheat_soil_pos: list[(int, int)] | None = self.get_wheat_soil_pos()
        

    def get_wheat_soil_pos(self):

        row, col = self.x, self.y
        print(self.game_controller)
        map = self.game_controller.get_map()
        if map[row][col].get_show_tile():
            return [
                (row + 1, col),
                (row + 1, col + 1),
                (row + 1, col + 2),
                (row, col + 2),
                (row - 1, col + 2)
            ]
        return None

    
