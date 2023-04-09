from enum import IntEnum

# IntEnum: 400 - 499 range

class NetworkCommandsTypes(IntEnum):
    CONNECT = 400
    DISCONNECT = 401
    GAME_SAVE = 402
    ASK_SAVE = 403

    BUILD = 410
    DELETE_BUILDING = 411
    RISK_UPDATE = 412

    UPDATE_WALKER = 420
    SPAWN_WALKER = 421
    DELETE_WALKER = 422

    DELEGATE = 499