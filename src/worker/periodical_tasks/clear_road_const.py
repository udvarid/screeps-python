from src.constant.my_constants import ROOM_CLEAR_ROAD_CONST_SITES
from src.defs import *
from src.utility.helper import get_active_rooms

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


def clear_road_const():
    if not Memory.counters["room_clear_road_const_sites"] or Memory.counters["room_clear_road_const_sites"] <= 0:
        time_limit = ROOM_CLEAR_ROAD_CONST_SITES
        __pragma__('js', '{}', 'Memory.counters["room_clear_road_const_sites"] = time_limit')
        for room_name in get_active_rooms():
            room = Game.rooms[room_name]
            road_const_sites = list(filter(lambda s: s.structureType == STRUCTURE_ROAD,
                                           room.find(FIND_CONSTRUCTION_SITES)))
            for road_const_site in road_const_sites:
                road_const_site.remove()
    else:
        actual = Memory.counters["room_clear_road_const_sites"]
        __pragma__('js', '{}', 'Memory.counters["room_clear_road_const_sites"] = actual - 1')


