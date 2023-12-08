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
    if not Memory.rampart_time or Memory.rampart_time <= 0:
        Memory.rampart_time = ROOM_RAMPART
        for room_name in Object.keys(Game.rooms):
            room = Game.rooms[room_name]
            if len(room.find(FIND_MY_SPAWNS)) > 0:
                construction_sites = room.find(FIND_MY_CONSTRUCTION_SITES)
                towers = filter(lambda s: s.structureType == STRUCTURE_TOWER, room.find(FIND_MY_STRUCTURES))
                if len(construction_sites) == 0 and len(towers) > 0:
                    vip_structures = filter(lambda s: STRUCTURES_NEED_RAMPART.includes(s.structureType),
                                            room.find(FIND_MY_STRUCTURES))
                    ramparts = filter(lambda s: s.structureType == STRUCTURE_RAMPART, room.find(FIND_MY_STRUCTURES))
                    for vip in vip_structures:
                        if not any(vip.pos.x == rampart.pos.x and vip.pos.y == rampart.pos.y for rampart in ramparts):
                            room.createConstructionSite(vip.pos.x, vip.pos.y, STRUCTURE_RAMPART)
                            return
    else:
        Memory.rampart_time -= 1
