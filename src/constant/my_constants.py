from src.defs import *
from src.roles.spawn_roles.harvester_logic import need_extra as harvest_logic
from src.roles.spawn_roles.builder_logic import need_extra as builder_logic

MEMORY_CLEANING = 1000

SPAWN_PLAN = {
    'harvester': {
        'min': 8,
        'base_body': [WORK, CARRY, MOVE, MOVE],
        'logic': harvest_logic
    },
    'builder': {
        'min': 0,
        'base_body': [WORK, CARRY, MOVE, MOVE],
        'logic': builder_logic
    }
}
