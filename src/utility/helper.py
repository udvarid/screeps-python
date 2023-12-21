from src.defs import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


def get_active_rooms():
    my_rooms = []
    for room_name in Object.keys(Game.rooms):
        room = Game.rooms[room_name]
        spawns = room.find(FIND_MY_SPAWNS)
        if len(spawns) > 0:
            my_rooms.append(room_name)
    return my_rooms


def get_full_neighbours(actual):
    x = actual[0]
    y = actual[1]

    n1 = (x - 1, y - 1)
    n2 = (x - 1, y)
    n3 = (x - 1, y + 1)

    n4 = (x, y - 1)
    n5 = (x, y + 1)

    n6 = (x + 1, y - 1)
    n7 = (x + 1, y)
    n8 = (x + 1, y + 1)
    return [n1, n2, n3, n4, n5, n6, n7, n8]
