from src.constant.my_constants import ROOM_CONQUER
from src.utility.helper import get_active_rooms
from src.defs import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


def check_for_new_conquers():
    if not Memory.counters["conquer_time"] or Memory.counters["conquer_time"] <= 0:
        time_limit = ROOM_CONQUER
        __pragma__('js', '{}', 'Memory.counters["conquer_time"] = time_limit')
        my_rooms = get_active_rooms()
        if len(my_rooms) >= Game.gcl.level:
            return

        room_conquer = {}
        if Memory.room_conquer is undefined:
            Memory.room_conquer = room_conquer

        my_free_rooms = get_free_rooms(my_rooms)

        clean_old_conquers()

        for room_map in Object.keys(Memory.room_map):
            old = Game.time - Memory.room_map[room_map]['time'] > 15000
            energy = Memory.room_map[room_map]['energy'] == 2
            free = Memory.room_map[room_map]['owner'] == "free"
            secured = Memory.room_map[room_map]['enemy'] is False and Memory.room_map[room_map]['attacker'] is False
            under_occupy = check_under_occupy(room_map)
            if not old and energy and free and secured and not under_occupy:
                occupier = get_occupier(my_free_rooms, Memory.room_map[room_map]['neighbours'])
                if occupier is not undefined:
                    print("Room {} should be occupied by {}".format(room_map, occupier))
                    aim = {
                        'aim': room_map,
                        'claimed': False,
                        'time': Game.time
                    }
                    __pragma__('js', '{}', 'Memory.room_conquer[occupier] = aim')
    else:
        actual = Memory.counters["conquer_time"]
        __pragma__('js', '{}', 'Memory.counters["conquer_time"] = actual - 1')


def clean_old_conquers():
    for occupier in Object.keys(Memory.room_conquer):
        occupy = Memory.room_conquer[occupier]
        if Game.time - occupy['time'] > 50000:
            del Memory.room_conquer[occupier]


def get_occupier(rooms, neighbours):
    occupier = undefined
    if any(neighbours['up'] == room for room in rooms):
        occupier = neighbours['up']
    elif any(neighbours['bottom'] == room for room in rooms):
        occupier = neighbours['bottom']
    elif any(neighbours['right'] == room for room in rooms):
        occupier = neighbours['right']
    elif any(neighbours['left'] == room for room in rooms):
        occupier = neighbours['left']
    return occupier


def get_free_rooms(my_rooms):
    cleaned_rooms = []
    for my_room in my_rooms:
        room = Memory.room_conquer[my_room]
        if Memory.room_conquer[my_room] is undefined and \
                room.controller.level >= 7 and \
                len(room.find(FIND_MY_SPAWNS)) > 1 and \
                room.storage is not undefined and \
                room.storage.store[RESOURCE_ENERGY] > 100000:
            cleaned_rooms.append(my_room)
    return cleaned_rooms


def check_under_occupy(room_map):
    for occupier in Object.keys(Memory.room_conquer):
        operation = Memory.room_conquer[occupier]
        if operation['aim'] == room_map:
            return True
    return False
