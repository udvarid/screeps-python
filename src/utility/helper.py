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
        if len(spawns) > 0 and room.controller.my:
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


def get_link_with_energy(room_name):
    central_link_id = Memory.links[room_name]
    if central_link_id is not undefined:
        link = Game.getObjectById(central_link_id)
        if link is not None and link.energy > 0:
            return link
    return None


def route_maintaining(creep):
    route_here = list(filter(lambda s: s.structureType == STRUCTURE_ROAD,
                             creep.pos.findInRange(FIND_STRUCTURES, 0)))
    if len(route_here) == 0:
        const_site_here = list(creep.pos.findInRange(FIND_CONSTRUCTION_SITES, 0))
        if len(const_site_here) == 0:
            creep.room.createConstructionSite(creep.pos.x, creep.pos.y, STRUCTURE_ROAD)
        else:
            road_const_here = list(filter(lambda s: s.structureType == STRUCTURE_ROAD,
                                          creep.pos.findInRange(FIND_CONSTRUCTION_SITES, 0)))
            if len(road_const_here) != 0:
                creep.build(road_const_here[0])
    else:
        route = route_here[0]
        if route.hits < route.hitsMax * 0.75:
            creep.repair(route)
