from src.constant.my_constants import ROOM_MINE
from src.defs import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


def construct_mine():
    if not Memory.counters["mine_time"] or Memory.counters["mine_time"] <= 0:
        time_limit = ROOM_MINE
        __pragma__('js', '{}', 'Memory.counters["mine_time"] = time_limit')
        for room_name in Object.keys(Game.rooms):
            room = Game.rooms[room_name]
            spawns = room.find(FIND_MY_SPAWNS)
            if len(spawns) > 0:
                if room.controller.level < 6:
                    continue
                construction_sites = list(filter(lambda c: c.structureType != STRUCTURE_ROAD,
                                                 room.find(FIND_MY_CONSTRUCTION_SITES)))
                extractors = list(filter(lambda s: s.structureType == STRUCTURE_EXTRACTOR,
                                         room.find(FIND_MY_STRUCTURES)))
                if len(construction_sites) == 0 and len(extractors) == 0:
                    mine = room.find(FIND_MINERALS)[0]
                    room.createConstructionSite(mine.pos.x, mine.pos.y, STRUCTURE_EXTRACTOR)
                    print("Creating mine at {}".format(mine.pos))
    else:
        actual = Memory.counters["mine_time"]
        __pragma__('js', '{}', 'Memory.counters["mine_time"] = actual - 1')
