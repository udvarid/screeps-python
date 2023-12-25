from src.constant.my_constants import ROOM_LINK
from src.worker.periodical_tasks.create_construction_site import is_valid_type, is_near_to_sources, pos_in_the_frame
from src.defs import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


def construct_links():
    if Memory.links is undefined:
        Memory.links = {}
    if not Memory.counters["link_time"] or Memory.counters["link_time"] <= 0:
        __pragma__('js', '{}', 'Memory.counters["link_time"] = ROOM_LINK')
        for room_name in Object.keys(Game.rooms):
            room = Game.rooms[room_name]
            spawns = room.find(FIND_MY_SPAWNS)
            if len(spawns) > 0:
                if room.controller.level < 6:
                    continue
                construction_sites = room.find(FIND_MY_CONSTRUCTION_SITES)
                links = list(filter(lambda s: s.structureType == STRUCTURE_LINK, room.find(FIND_MY_STRUCTURES)))
                if len(construction_sites) == 0 and len(links) < 3:
                    check_and_build_at_store(room, spawns[0], links)
                    check_and_build_at_sources(room, spawns[0], links)
                if len(links) > 0:
                    put_central_link_id_into_memory(room, links)
    else:
        actual = Memory.counters["link_time"]
        __pragma__('js', '{}', 'Memory.counters["link_time"] = actual - 1')


def put_central_link_id_into_memory(room, links):
    storage = room.storage
    if storage is not undefined:
        for link in links:
            if storage.pos.isNearTo(link):
                link_id = link.id
                room_name = room.name
                __pragma__('js', '{}', 'Memory.links[room_name] = link_id')
                return


def check_and_build_at_store(room, spawn, links):
    storage = room.storage
    if storage is not undefined:
        if any(storage.pos.isNearTo(link) for link in links):
            return
        neighbours = [
            (storage.pos.x - 1, storage.pos.y),
            (storage.pos.x + 1, storage.pos.y),
            (storage.pos.x, storage.pos.y - 1),
            (storage.pos.x, storage.pos.y + 1)
        ]
        filtered_neighbours = map(lambda f: __new__(RoomPosition(f[0], f[1], room.name)),
                                  list(filter(lambda n: is_valid_type(n, room) and
                                                        not is_near_to_sources(n, room), neighbours)))
        closest = spawn.pos.findClosestByPath(filtered_neighbours)
        room.createConstructionSite(closest.x, closest.y, STRUCTURE_LINK)
        print("Create construction site at {}".format(closest))


def check_and_build_at_sources(room, spawn, links):
    sources = room.find(FIND_SOURCES)
    for source in sources:
        sp = source.pos
        if any(sp.inRangeTo(link, 2) for link in links):
            return
        neighbours = [
            (sp.x - 2, sp.y),
            (sp.x - 2, sp.y - 1),
            (sp.x - 2, sp.y - 2),
            (sp.x - 2, sp.y + 1),
            (sp.x - 2, sp.y + 2),
            (sp.x + 2, sp.y),
            (sp.x + 2, sp.y - 1),
            (sp.x + 2, sp.y - 2),
            (sp.x + 2, sp.y + 1),
            (sp.x + 2, sp.y + 2),
            (sp.x, sp.y - 2),
            (sp.x - 1, sp.y - 2),
            (sp.x + 1, sp.y - 2),
            (sp.x, sp.y + 2),
            (sp.x - 1, sp.y + 2),
            (sp.x + 1, sp.y + 2)
        ]
        filtered_neighbours = map(lambda f: __new__(RoomPosition(f[0], f[1], room.name)),
                                  list(filter(lambda n: is_valid_type(n, room) and pos_in_the_frame(n) and
                                                        not is_near_to_sources(n, room), neighbours)))
        closest = spawn.pos.findClosestByPath(filtered_neighbours)
        room.createConstructionSite(closest.x, closest.y, STRUCTURE_LINK)
        print("Create construction site at {}".format(closest))
