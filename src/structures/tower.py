
from src.defs import *


__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


def operate_towers():
    for room_name in Object.keys(Game.rooms):
        room = Game.rooms[room_name]
        towers = filter(lambda s: s.structureType == STRUCTURE_TOWER and s.energyCapacity > 0,
                        room.find(FIND_MY_STRUCTURES))
        for tower in towers:
            operate_tower(tower)


def operate_tower(tower):
    closest_enemy = tower.pos.findClosestByRange(FIND_HOSTILE_CREEPS)
    if closest_enemy is not None:
        tower.attack(closest_enemy)
        return
    # TODO try tho heal
    # TODO try to repair
    # TODO build rampart and walls

