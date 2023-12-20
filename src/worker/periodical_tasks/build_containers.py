from src.constant.my_constants import ROOM_CONTAINER
from src.worker.periodical_tasks.create_construction_site import is_valid_type, pos_in_the_frame
from src.defs import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


def construct_containers():
    if not Memory.container_time or Memory.container_time <= 0:
        Memory.container_time = ROOM_CONTAINER
        for room_name in Object.keys(Game.rooms):
            room = Game.rooms[room_name]
            spawns = room.find(FIND_MY_SPAWNS)
            if len(spawns) > 0:
                construction_sites = room.find(FIND_MY_CONSTRUCTION_SITES)
                containers = list(filter(lambda s: s.structureType == STRUCTURE_CONTAINER, room.find(FIND_STRUCTURES)))
                extractors = list(
                    filter(lambda s: s.structureType == STRUCTURE_EXTRACTOR, room.find(FIND_MY_STRUCTURES)))
                if len(construction_sites) == 0 and len(containers) < 3 and len(extractors) > 0:
                    check_and_build(spawns[0], containers, extractors[0])
    else:
        Memory.container_time -= 1


def check_and_build(spawn, containers, extractor):
    ex_pos = extractor.pos
    neighbours = [
        (ex_pos.x - 1, ex_pos.y - 1),
        (ex_pos.x - 1, ex_pos.y),
        (ex_pos.x - 1, ex_pos.y + 1),
        (ex_pos.x, ex_pos.y - 1),
        (ex_pos.x, ex_pos.y + 1),
        (ex_pos.x + 1, ex_pos.y - 1),
        (ex_pos.x + 1, ex_pos.y),
        (ex_pos.x + 1, ex_pos.y + 1),
    ]

    room = spawn.room
    filtered_neighbours = list(map(lambda f: __new__(RoomPosition(f[0], f[1], room.name)),
                                   list(filter(lambda n: is_valid_type(n, room) and pos_in_the_frame(n) and
                                                         not is_container_at_position(n, containers), neighbours))))
    if len(filtered_neighbours) > 0:
        closest = spawn.pos.findClosestByPath(filtered_neighbours)
        room.createConstructionSite(closest.x, closest.y, STRUCTURE_CONTAINER)
        print("Create construction site at {}".format(closest))


def is_container_at_position(position, containers):
    return any(position[0] == cont.pos.x and position[1] == cont.pos.y for cont in containers)
