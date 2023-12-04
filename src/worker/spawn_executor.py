from src.roles.spawn_roles.upgrader_logic import need_extra as upgrader_logic
from src.roles.spawn_roles.harvester_logic import need_extra as harvest_logic
from src.roles.spawn_roles.builder_logic import need_extra as builder_logic

from src.defs import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')

SPAWN_PLAN = {
    'harvester': {
        'min': 2,
        'max': 8,
        'base_body': [WORK, CARRY, MOVE, MOVE],
        'logic': harvest_logic
    },
    'builder': {
        'min': 0,
        'max': 2,
        'base_body': [WORK, CARRY, MOVE, MOVE],
        'logic': builder_logic
    },
    'upgrader': {
        'min': 0,
        'max': 2,
        'base_body': [WORK, CARRY, MOVE, MOVE],
        'logic': upgrader_logic
    }
}


def do_spawn():
    for name in Object.keys(Game.spawns):
        spawn = Game.spawns[name]
        energy_capacity = spawn.room.energyAvailable
        if not spawn.spawning and energy_capacity >= 250:
            for role_name in Object.keys(SPAWN_PLAN):
                role = SPAWN_PLAN[role_name]
                num_role_creeps = _.sum(Game.creeps, lambda c: c.pos.roomName == spawn.pos.roomName and
                                                               c.memory.role == role_name)
                context = {
                    'room': spawn.room,
                    'max': role.max,
                    'number': num_role_creeps
                }
                if num_role_creeps < role.min or role.logic(context):
                    multiplier = calculate_multiplier(energy_capacity, role.base_body)
                    body_list = role.base_body[:]
                    if multiplier > 1:
                        for i in range(min(multiplier, 5) - 1):
                            body_list.extend(role.base_body)
                    name = "{}{}".format(role_name, Game.time)
                    spawn.spawnCreep(body_list, name, {'memory': {'role': role_name}})
                    return


def calculate_multiplier(capacity, body_parts):
    cost = 0
    for body_part in body_parts:
        cost += BODYPART_COST[body_part]
    return capacity // cost
