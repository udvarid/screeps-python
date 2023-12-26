from src.constant.my_constants import ROOM_CLEAR
from src.defs import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


def clear_walls():
    if not Memory.counters["clear_time"] or Memory.counters["clear_time"] <= 0:
        time_limit = ROOM_CLEAR
        __pragma__('js', '{}', 'Memory.counters["clear_time"] = time_limit')
        print("Unknown wall clearing")
        for room_name in Object.keys(Game.rooms):
            room = Game.rooms[room_name]
            if len(room.find(FIND_MY_SPAWNS)) > 0 and (not Memory.room_clear or not Memory.room_clear[room_name]):
                walls = list(filter(lambda s: s.structureType == STRUCTURE_WALL, room.find(FIND_STRUCTURES)))
                if len(walls) > 0:
                    wall = walls[0]
                    print("Deleting wall at x:{}, y:{}".format(wall.pos.x, wall.pos.y))
                    wall.destroy()
                else:
                    if not Memory.room_clear:
                        room_snapshot = {room_name: 'CLEARED'}
                        __pragma__('js', '{}', 'Memory.room_clear = room_snapshot')
                    else:
                        __pragma__('js', '{}', 'Memory.room_clear[room_name] = "CLEARED"')

    else:
        actual = Memory.counters["clear_time"]
        __pragma__('js', '{}', 'Memory.counters["clear_time"] = actual - 1')

