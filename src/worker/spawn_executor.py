from src.roles.spawn_roles.hauler_logic import need_extra as hauler_logic
from src.roles.spawn_roles.upgrader_logic import need_extra as upgrader_logic
from src.roles.spawn_roles.harvester_logic import need_extra as harvest_logic
from src.roles.spawn_roles.builder_logic import need_extra as builder_logic
from src.roles.spawn_roles.miner_logic import need_extra as miner_logic
from src.roles.spawn_roles.scouter_logic import need_extra as scouter_logic, give_aim as give_scouter_aim
from src.roles.spawn_roles.claimer_logic import need_extra as claimer_logic, give_aim as give_claimer_aim
from src.roles.spawn_roles.c_builder_logic import need_extra as c_builder_logic, give_aim as give_c_builder_aim

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
    'claimer': {
        'min': 0,
        'max': 0,
        'base_body': [MOVE, MOVE, MOVE, MOVE, MOVE, MOVE, MOVE, CLAIM],
        'logic': claimer_logic,
        'multiple': False,
        'aim_logic': give_claimer_aim
    },
    'c_builder': {
        'min': 0,
        'max': 0,
        'base_body': [WORK, CARRY, MOVE, MOVE, WORK, CARRY, MOVE, MOVE,
                      WORK, CARRY, MOVE, MOVE, WORK, CARRY, MOVE, MOVE],
        'logic': c_builder_logic,
        'multiple': False,
        'aim_logic': give_c_builder_aim
    },
    'hauler': {
        'min': 0,
        'max': 2,
        'base_body': [CARRY, CARRY, MOVE, MOVE],
        'logic': hauler_logic,
        'multiple': True
    },
    'harvester': {
        'min': 2,
        'max': 8,
        'base_body': [WORK, CARRY, MOVE, MOVE],
        'logic': harvest_logic,
        'multiple': True
    },
    'builder': {
        'min': 0,
        'max': 1,
        'base_body': [WORK, CARRY, MOVE, MOVE],
        'logic': builder_logic,
        'multiple': True
    },
    'upgrader': {
        'min': 0,
        'max': 3,
        'base_body': [WORK, CARRY, MOVE, MOVE],
        'logic': upgrader_logic,
        'multiple': True
    },
    'miner': {
        'min': 0,
        'max': 2,
        'base_body': [WORK, CARRY, MOVE, MOVE],
        'logic': miner_logic,
        'multiple': True
    },
    'scouter': {
        'min': 0,
        'max': 1,
        'base_body': [MOVE],
        'logic': scouter_logic,
        'multiple': False,
        'aim_logic': give_scouter_aim
    }
}


def do_spawn():
    for name in Object.keys(Game.spawns):
        spawn = Game.spawns[name]
        energy_capacity = spawn.room.energyAvailable
        if not spawn.spawning and energy_capacity >= 250:
            for role_name in Object.keys(SPAWN_PLAN):
                role = SPAWN_PLAN[role_name]
                num_role_creeps = _.sum(Game.creeps, lambda c: c.memory.home == spawn.pos.roomName and
                                                               c.memory.role == role_name)
                context = {
                    'room': spawn.room,
                    'max': role.max,
                    'number': num_role_creeps
                }
                if num_role_creeps < role.min or role.logic(context):
                    multiplier = 1 if role.multiple is False else calculate_multiplier(energy_capacity, role.base_body)
                    body_list = role.base_body[:]
                    if multiplier > 1:
                        for i in range(min(multiplier, 10) - 1):
                            body_list.extend(role.base_body)
                    name = "{}{}".format(role_name, Game.time)
                    aim_name = spawn.room.name if role.aim_logic is undefined else role.aim_logic(spawn.room.name)
                    memory = {
                        'memory': {
                            'role': role_name,
                            'home': spawn.room.name,
                            'aim': aim_name
                        }
                    }
                    spawn.spawnCreep(body_list, name, memory)
                    return


def calculate_multiplier(capacity, body_parts):
    cost = 0
    for body_part in body_parts:
        cost += BODYPART_COST[body_part]
    return capacity // cost
