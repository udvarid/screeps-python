from src.constant.my_constants import ROOM_MAP_MAKING
from src.defs import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


def check_for_new_rooms():
    if not Memory.scout_time or Memory.scout_time <= 0:
        room_maps = {}
        if Memory.room_map is undefined:
            Memory.room_map = room_maps
        Memory.scout_time = ROOM_MAP_MAKING
        for room_name in Object.keys(Game.rooms):
            room = Game.rooms[room_name]
            spawns = room.find(FIND_MY_SPAWNS)
            if len(spawns) > 0:
                is_there_enemy = Memory.room_safety_state[room_name].enemy
                is_there_attacker = Memory.room_safety_state[room_name].attacker
                previous_state = Memory.room_map[room_name]
                if previous_state is undefined or previous_state['neighbours'] is undefined:
                    neighbours = get_neighbours(room)
                else:
                    neighbours = previous_state['neighbours']
                room_state = {
                    'energy': 2,
                    'owner': 'me',
                    'enemy': is_there_enemy,
                    'attacker': is_there_attacker,
                    'neighbours': neighbours,
                    'time': Game.time
                }
                __pragma__('js', '{}', 'Memory.room_map[room_name] = room_state')

    else:
        Memory.scout_time -= 1


def get_neighbours(room):
    neighbours = {}
    sign = "?" if len(room.find(FIND_EXIT_TOP)) > 0 else "NO"
    __pragma__('js', '{}', 'neighbours["up"] = sign')

    sign = "?" if len(room.find(FIND_EXIT_BOTTOM)) > 0 else "NO"
    __pragma__('js', '{}', 'neighbours["bottom"] = sign')

    sign = "?" if len(room.find(FIND_EXIT_RIGHT)) > 0 else "NO"
    __pragma__('js', '{}', 'neighbours["right"] = sign')

    sign = "?" if len(room.find(FIND_EXIT_LEFT)) > 0 else "NO"
    __pragma__('js', '{}', 'neighbours["left"] = sign')
    return neighbours
