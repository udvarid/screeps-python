from src.constant.my_constants import ROOM_SAFETY
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
                safety_check[room_name] = {
                    'enemy': len(enemies) > 0,
                    'attacker': len(attacker_enemies) > 0
                }
        Memory.room_safety_state = safety_check
    else:
        Memory.room_safety_check_time -= 1
