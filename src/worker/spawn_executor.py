from src.constant.my_constants import SPAWN_PLAN
from src.defs import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


def do_spawn():
    for name in Object.keys(Game.spawns):
        spawn = Game.spawns[name]
        energy_capacity = spawn.room.energyAvailable
        if not spawn.spawning and energy_capacity >= 250:
            context = {
                'room': spawn.room
            }
            for role_name in Object.keys(SPAWN_PLAN):
                role = SPAWN_PLAN[role_name]
                num_role_creeps = _.sum(Game.creeps, lambda c: c.pos.roomName == spawn.pos.roomName and
                                                               c.memory.role == role_name)
                if num_role_creeps < role.min or role.logic(context):
                    multiplier = calculate_multiplier(energy_capacity, role.base_body)
                    body_list = []
                    if multiplier > 1:
                        body_list = role.base_body
                        for i in range(min(multiplier, 4)):
                            body_list = [*body_list, *role.base_body]
                    name = "{}{}".format(role_name, Game.time)
                    spawn.spawnCreep(body_list, name, {'memory': {'role': role_name}})


def calculate_multiplier(capacity, body_parts):
    cost = 0
    for body_part in body_parts:
        cost += BODYPART_COST[body_part]
    return capacity // cost
