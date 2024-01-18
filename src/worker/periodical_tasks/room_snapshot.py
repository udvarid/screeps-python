from src.constant.my_constants import ROOM_SNAPSHOT
from src.defs import *
from src.utility.helper import get_full_neighbours
from src.worker.periodical_tasks.create_construction_site import is_valid_type

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


def make_room_snapshot():
    if not Memory.counters["room_snapshot_time"] or Memory.counters["room_snapshot_time"] <= 0:
        time_limit = ROOM_SNAPSHOT
        __pragma__('js', '{}', 'Memory.counters["room_snapshot_time"] = time_limit')
        print("Making room snapshots")
        snapshot = {}
        for room_name in Object.keys(Game.rooms):
            room = Game.rooms[room_name]
            if len(room.find(FIND_MY_SPAWNS)) > 0 and room.controller.my:
                prev_mine_place = undefined
                prev_source_place = undefined
                prev_hauler_time = undefined
                if Memory.room_snapshot is not undefined and Memory.room_snapshot[room_name] is not undefined:
                    prev_mine_place = Memory.room_snapshot[room_name]['mine_place']
                    prev_source_place = Memory.room_snapshot[room_name]['source_place']
                    prev_hauler_time = Memory.room_snapshot[room_name]['hauler_time']
                    prev_mine_type = Memory.room_snapshot[room_name]['mineral']
                if prev_mine_place is undefined:
                    free_mine_places = get_free_mine_places(room)
                else:
                    free_mine_places = prev_mine_place
                if prev_source_place is undefined:
                    free_source_places = get_free_source_places(room)
                else:
                    free_source_places = prev_source_place
                if prev_mine_type is undefined:
                    mine_type = room.find(FIND_MINERALS)[0].mineralType
                else:
                    mine_type = prev_mine_type
                room_snapshot = {
                    'energy': room.energyAvailable,
                    'mineral': mine_type,
                    'mine_place': free_mine_places,
                    'source_place': free_source_places
                }
                if prev_hauler_time is not undefined:
                    __pragma__('js', '{}', 'room_snapshot["hauler_time"] = prev_hauler_time')
                __pragma__('js', '{}', 'snapshot[room_name] = room_snapshot')
        Memory.room_snapshot = snapshot
    else:
        actual = Memory.counters["room_snapshot_time"]
        __pragma__('js', '{}', 'Memory.counters["room_snapshot_time"] = actual - 1')


def get_free_mine_places(room):
    mine = room.find(FIND_MINERALS)[0]
    neighbours = get_full_neighbours((mine.pos.x, mine.pos.y))
    free_places = []
    for neighbour in neighbours:
        if pos_in_the_frame_for_free_places(neighbour) and is_valid_type(neighbour, room):
            free_places.append(neighbour)
    return len(free_places)


def get_free_source_places(room):
    sources = room.find(FIND_SOURCES)
    free_places = []
    for source in sources:
        neighbours = get_full_neighbours((source.pos.x, source.pos.y))
        for neighbour in neighbours:
            if pos_in_the_frame_for_free_places(neighbour) and is_valid_type(neighbour, room):
                free_places.append(neighbour)
    return len(free_places)


def pos_in_the_frame_for_free_places(position):
    return not (position[0] < 2 or position[0] > 47 or position[1] < 2 or position[1] > 47)
