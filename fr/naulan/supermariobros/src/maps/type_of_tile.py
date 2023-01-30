from enum import Enum


class TypeOfTile(Enum):
    EMPTY = -1
    PLATFORM = 1
    FLOORS = 2
    BUSH = 3
    LOOT_BLOCK = 4
    CLOUD = 5