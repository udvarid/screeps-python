from src.constant.my_constants import ROOM_SNAPSHOT
from src.defs import *
from src.utility.helper import get_full_neighbours
from src.worker.periodical_tasks.create_construction_site import pos_in_the_frame, is_valid_type

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
            if len(room.find(FIND_MY_SPAWNS)) > 0 and room.controller.my:
                mine = room.find(FIND_MINERALS)[0]
                prev_mine_place = undefined
                prev_source_place = undefined
                if Memory.room_snapshot is not undefined and Memory.room_snapshot[room_name] is not undefined:
                    prev_mine_place = Memory.room_snapshot[room_name]['mine_place']
                    prev_source_place = Memory.room_snapshot[room_name]['source_place']
                free_mine_places = prev_mine_place if prev_mine_place is not undefined else get_free_mine_places(room)
                free_source_places = prev_source_place if prev_source_place is not undefined else get_free_source_places(
                    room)
                room_snapshot = {
                    'energy': room.energyAvailable,
                    'mineral': mine.mineralType,
                    'mine_place': free_mine_places,
                    'source_place': free_source_places
                }
                __pragma__('js', '{}', 'snapshot[room_name] = room_snapshot')
        Memory.room_snapshot = snapshot
    else:
        Memory.room_snapshot_time -= 1


def get_free_mine_places(room):
    mine = room.find(FIND_MINERALS)[0]
    neighbours = get_full_neighbours((mine.pos.x, mine.pos.y))
    free_places = []
    for neighbour in neighbours:
        if pos_in_the_frame(neighbour) and is_valid_type(neighbour, room):
            free_places.append(neighbour)
    return len(free_places)


def get_free_source_places(room):
    sources = room.find(FIND_SOURCES)
    free_places = []
    for source in sources:
        neighbours = get_full_neighbours((source.pos.x, source.pos.y))
        for neighbour in neighbours:
            if pos_in_the_frame(neighbour) and is_valid_type(neighbour, room):
                free_places.append(neighbour)
    return len(free_places)
