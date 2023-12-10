from src.defs import *


MEMORY_CLEANING = 1000
ROOM_SNAPSHOT = 300
ROOM_SAFETY = 10
ROOM_RAMPART = 500
ROOM_CLEAR = 500
ROOM_CONSTRUCTION = 500

FILL_WITH_ENERGY = [STRUCTURE_SPAWN, STRUCTURE_EXTENSION, STRUCTURE_TOWER]
FILL_WITH_ENERGY_WO_TOWER = [STRUCTURE_SPAWN, STRUCTURE_EXTENSION]
STRUCTURES_NOT_TO_HEAL = [STRUCTURE_WALL, STRUCTURE_RAMPART, STRUCTURE_ROAD, STRUCTURE_CONTAINER]
STRUCTURE_WALL_OR_RAMPART_OR_ROAD = [STRUCTURE_WALL, STRUCTURE_RAMPART, STRUCTURE_ROAD]
STRUCTURE_WALL_OR_RAMPART = [STRUCTURE_WALL, STRUCTURE_RAMPART]
STRUCTURES_NEED_RAMPART = [
    STRUCTURE_SPAWN,
    STRUCTURE_TOWER,
    STRUCTURE_STORAGE,
    STRUCTURE_TERMINAL
]
STRUCTURES_NEED_CONSTRUCT = [
    STRUCTURE_SPAWN,
    STRUCTURE_TOWER,
    STRUCTURE_EXTENSION,
    STRUCTURE_STORAGE,
    STRUCTURE_TERMINAL
]

RAMPART_AND_WALL_SIZE = [
    0,
    100000,
    250000,
    500000,
    1000000,
    2500000,
    5000000,
    10000000
]
