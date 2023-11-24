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
        if not spawn.spawning and spawn.room.energyCapacityAvailable >= 250:
            context = {}  # TODO feltölteni általános adatokkal
            for role_name in Object.keys(SPAWN_PLAN):
                role = SPAWN_PLAN[role_name]
                num_role_creeps = _.sum(Game.creeps, lambda c: c.pos.roomName == spawn.pos.roomName and
                                                               c.memory.role == role_name)
                if num_role_creeps < role.min or role.logic(context):
                    # TODO kiszámolni a költségét és max 4 szeresére felnövelni az alap tervet, ha belefér
                    name = "{}{}".format(role_name, Game.time)
                    spawn.spawnCreep(role.base_body, name, {'memory': {'role': role_name}})
