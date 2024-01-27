from src.constant.my_constants import ROOM_RAMPART, STRUCTURES_NEED_RAMPART
from src.defs import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


def create_rampart():
    if not Memory.counters["rampart_time"] or Memory.counters["rampart_time"] <= 0:
        time_limit = ROOM_RAMPART
        __pragma__('js', '{}', 'Memory.counters["rampart_time"] = time_limit')
        for room_name in Object.keys(Game.rooms):
            room = Game.rooms[room_name]
            if len(room.find(FIND_MY_SPAWNS)) > 0:
                construction_sites = list(filter(lambda c: c.structureType != STRUCTURE_ROAD,
                                                 room.find(FIND_MY_CONSTRUCTION_SITES)))
                towers = list(filter(lambda s: s.structureType == STRUCTURE_TOWER, room.find(FIND_MY_STRUCTURES)))
                storage = room.storage
                have_energy = True
                if storage is not undefined and storage.store.getUsedCapacity(RESOURCE_ENERGY) < 125000:
                    have_energy = False
                if len(construction_sites) == 0 and len(towers) > 0 and have_energy:
                    vip_structures = list(filter(lambda s: STRUCTURES_NEED_RAMPART.includes(s.structureType),
                                                 room.find(FIND_MY_STRUCTURES)))
                    ramparts = list(filter(lambda s: s.structureType == STRUCTURE_RAMPART,
                                           room.find(FIND_MY_STRUCTURES)))
                    for vip in vip_structures:
                        if not any(vip.pos.x == rampart.pos.x and vip.pos.y == rampart.pos.y for rampart in ramparts):
                            room.createConstructionSite(vip.pos.x, vip.pos.y, STRUCTURE_RAMPART)
    else:
        actual = Memory.counters["rampart_time"]
        __pragma__('js', '{}', 'Memory.counters["rampart_time"] = actual - 1')

