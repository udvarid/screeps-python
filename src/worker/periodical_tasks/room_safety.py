from src.constant.my_constants import ROOM_SAFETY, STRUCTURE_NOT_TO_HEAL
from src.defs import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


def make_room_safety_check():
    if not Memory.room_safety_check_time or Memory.room_safety_check_time <= 0:
        Memory.room_safety_check_time = ROOM_SAFETY
        safety_check = {}
        for room_name in Object.keys(Game.rooms):
            room = Game.rooms[room_name]
            if len(room.find(FIND_MY_SPAWNS)) > 0:
                enemies = room.find(FIND_HOSTILE_CREEPS)
                attacker_enemies = filter(lambda c: c.getActiveBodyparts(RANGED_ATTACK) +
                                                    c.getActiveBodyparts(ATTACK) > 0, enemies)
                wounded_creeps = filter(lambda c: c.hits < c.hitsMax, room.find(FIND_MY_CREEPS))
                wounded_structures = filter(lambda s: s.hits < s.hitsMax and
                                                      not STRUCTURE_NOT_TO_HEAL.includes(s.structureType),
                                            room.find(FIND_MY_STRUCTURES))
                weak_containers = filter(lambda s: s.hits < s.hitsMax * 0.9 and s.structureType == STRUCTURE_CONTAINER,
                                            room.find(FIND_MY_STRUCTURES))
                snapshot = {
                    'enemy': len(enemies) > 0,
                    'attacker': len(attacker_enemies) > 0,
                    'wounded_creeps': len(wounded_creeps) > 0,
                    'wounded_struc': len(wounded_structures) > 0 or len(weak_containers) > 0
                }
                __pragma__('js', '{}', 'safety_check[room_name] = snapshot')
        Memory.room_safety_state = safety_check
    else:
        Memory.room_safety_check_time -= 1
