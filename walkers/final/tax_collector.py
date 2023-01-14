from buildable.buildable import Buildable
from class_types.walker_types import WalkerTypes
from walkers.walker import Walker


class TaxCollector(Walker):
    def __init__(self, associated_building: 'Buildable'):
        super().__init__(WalkerTypes.TAX_COLLECTOR, associated_building)

