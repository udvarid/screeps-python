from src.constant.my_constants import ROOM_SAFETY, STRUCTURES_NOT_TO_HEAL
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
    if not Memory.counters["room_safety_check_time"] or Memory.counters["room_safety_check_time"] <= 0:
        time_limit = ROOM_SAFETY
        __pragma__('js', '{}', 'Memory.counters["room_safety_check_time"] = time_limit')
        safety_check = {}
        for room_name in Object.keys(Game.rooms):
            room = Game.rooms[room_name]
            if len(room.find(FIND_MY_SPAWNS)) > 0 and room.controller.my:
                enemies = room.find(FIND_HOSTILE_CREEPS)
                attacker_enemies = list(filter(lambda c: c.getActiveBodyparts(RANGED_ATTACK) +
                                                         c.getActiveBodyparts(ATTACK) > 0, enemies))
                wounded_creeps = list(filter(lambda c: c.hits < c.hitsMax, room.find(FIND_MY_CREEPS)))
                wounded_structures = list(filter(lambda s: s.hits < s.hitsMax and
                                                           not STRUCTURES_NOT_TO_HEAL.includes(s.structureType),
                                                 room.find(FIND_MY_STRUCTURES)))
                weak_containers = list(filter(lambda s: s.hits < s.hitsMax * 0.9 and
                                                        s.structureType == STRUCTURE_CONTAINER,
                                              room.find(FIND_STRUCTURES)))
                snapshot = {
                    'enemy': len(enemies) > 0,
                    'attacker': len(attacker_enemies) > 0,
                    'wounded_creeps': len(wounded_creeps) > 0,
                    'wounded_struc': len(wounded_structures) > 0 or len(weak_containers) > 0
                }
                __pragma__('js', '{}', 'safety_check[room_name] = snapshot')

                activate_safe_mode_when_needed(room)
        Memory.room_safety_state = safety_check
    else:
        actual = Memory.counters["room_safety_check_time"]
        __pragma__('js', '{}', 'Memory.counters["room_safety_check_time"] = actual - 1')


def activate_safe_mode_when_needed(room):
    if Memory.room_safety_state[room.name] is not undefined and \
            Memory.room_safety_state[room.name].attacker and \
            room.controller.safeMode is undefined and \
            room.controller.safeModeCooldown is undefined and \
            room.controller.safeModeAvailable > 0:
        towers = list(filter(lambda s: s.structureType == STRUCTURE_TOWER and s.energy > 0,
                             room.find(FIND_MY_STRUCTURES)))
        if len(towers) == 0:
            room.controller.activateSafeMode()
