from src.constant.my_constants import ROOM_RESERVED_ATTACK
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


def check_for_new_reserved_attack():
    if not Memory.counters["reserved_attack_time"] or Memory.counters["reserved_attack_time"] <= 0:
        time_limit = ROOM_RESERVED_ATTACK
        __pragma__('js', '{}', 'Memory.counters["reserved_attack_time"] = time_limit')
        my_rooms = get_active_rooms()

        room_reserved_attack = {}
        if Memory.room_reserved_attack is undefined:
            Memory.room_reserved_attack = room_reserved_attack

        my_free_rooms = get_free_rooms(my_rooms)

        clean_old_reserved_attacks()

        for room_map in Object.keys(Memory.room_map):
            old = Game.time - Memory.room_map[room_map]['time'] > 15000
            reserved = Memory.room_map[room_map]['owner'] == "reserved"
            enemy_present = Memory.room_map[room_map]['enemy'] is True
            under_attack = check_under_attack(room_map)
            if not old and not under_attack and (enemy_present or reserved):
                attacker = get_attacker(my_free_rooms, Memory.room_map[room_map]['neighbours'])
                if attacker is not undefined:
                    print("Room {} should be attacked by {}".format(room_map, attacker))
                    aim = {
                        'aim': room_map,
                        'spawn_status': 'INIT',
                        'time': Game.time
                    }
                    __pragma__('js', '{}', 'Memory.room_reserved_attack[attacker] = aim')
    else:
        actual = Memory.counters["reserved_attack_time"]
        __pragma__('js', '{}', 'Memory.counters["reserved_attack_time"] = actual - 1')


def clean_old_reserved_attacks():
    for attacker in Object.keys(Memory.room_reserved_attack):
        attacker = Memory.room_reserved_attack[attacker]
        aim_room = attacker['aim']
        aim_room_detailed = Memory.room_map[aim_room]
        reserved = aim_room_detailed['owner'] == "reserved"
        enemy_present = aim_room_detailed['enemy'] is True
        if not reserved and not enemy_present or Game.time - attacker['time'] > 50000:
            del Memory.room_reserved_attack[attacker]


def get_attacker(rooms, neighbours):
    attacker = undefined
    if any(neighbours['up'] == room for room in rooms):
        attacker = neighbours['up']
    elif any(neighbours['bottom'] == room for room in rooms):
        attacker = neighbours['bottom']
    elif any(neighbours['right'] == room for room in rooms):
        attacker = neighbours['right']
    elif any(neighbours['left'] == room for room in rooms):
        attacker = neighbours['left']
    return attacker


def get_free_rooms(my_rooms):
    cleaned_rooms = []
    for my_room in my_rooms:
        room = Game.rooms[my_room]
        if Memory.room_reserved_attack[my_room] is undefined and \
                len(room.find(FIND_MY_SPAWNS)) > 1 and \
                room.controller.level >= 7 and \
                room.storage is not undefined and \
                room.storage.store[RESOURCE_ENERGY] > 100000:
            cleaned_rooms.append(my_room)
    return cleaned_rooms


def check_under_attack(room_map):
    for attacker in Object.keys(Memory.room_reserved_attack):
        operation = Memory.room_reserved_attack[attacker]
        if operation['aim'] == room_map:
            return True
    return False
