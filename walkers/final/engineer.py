from buildable.buildable import Buildable
from buildable.house import House
from buildable.structure import Structure
from class_types.walker_types import WalkerTypes
from network_system.system_layer.read_write import SystemInterface
from walkers.walker import Walker




class Engineer(Walker):
    def __init__(self, associated_building: Buildable):
        super().__init__(WalkerTypes.ENGINEER, associated_building, max_walk_distance=10, roads_only=True)

    def update(self):
        super().update()
        tiles = self.current_tile.get_adjacente_tiles(2)
        for tile in tiles:
            build = tile.get_building()
            if build:
                if (isinstance(tile.get_building(), House) or isinstance(tile.get_building(), Structure)) and build.risk.get_dest_status() > 0:
                    tile.get_building().risk.reset_dest_risk()
                    SystemInterface.get_instance().send_risk_update(build.risk.get_fire_status(),build.risk.get_dest_status(),tile.get_coord())
