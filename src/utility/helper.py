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
