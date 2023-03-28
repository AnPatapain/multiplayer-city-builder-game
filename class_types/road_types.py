from enum import IntEnum

# IntEnum: 0 - 100 range
class RoadTypes(IntEnum):
    ALONE = 1

    # End of road
    TL_ALONE = 2
    TR_ALONE = 3
    BR_ALONE = 4
    BL_ALONE = 5

    # Diagonal road
    TL_TO_BR = 6
    TR_TO_BL = 7

    # Angle road
    TL_TO_TR = 8
    TR_TO_BR = 9
    BR_TO_BL = 10
    BL_TO_TL = 11

    # Triple road
    TL_TO_TR_TO_BR = 12
    TR_TO_BR_TO_BL = 13
    BR_TO_BL_TO_TL = 14
    BL_TO_TL_TO_TR = 15

    # X road
    ALL_DIRECTION = 16
