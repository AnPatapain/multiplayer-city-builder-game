from buildable.buildable import Buildable
from class_types.walker_types import WalkerTypes
from walkers.walker import Walker
from game.id import ID_GEN

class TaxCollector(Walker):
    def __init__(self, associated_building: 'Buildable', player_id:int=0, id:int=0 ):
        super().__init__(WalkerTypes.TAX_COLLECTOR, associated_building)
        id_create = ID_GEN()
        self.id = id_create.id_gen()

