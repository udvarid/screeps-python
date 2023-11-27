from src.constant.my_constants import ROOM_SNAPSHOT
from src.defs import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


def make_room_snapshot():
    if not Memory.room_snapshot_time or Memory.room_snapshot_time <= 0:
        Memory.room_snapshot_time = ROOM_SNAPSHOT
        print("Making room snapshots")
        snapshot = {}
        for room_name in Object.keys(Game.rooms):
            room = Game.rooms[room_name]
            if len(room.find(FIND_MY_SPAWNS)) > 0:
                room_snapshot = {'energy': room.energyAvailable}
                __pragma__('js', '{}', 'snapshot[room_name] = room_snapshot')
        Memory.room_snapshot = snapshot
    else:
        Memory.room_snapshot_time -= 1
