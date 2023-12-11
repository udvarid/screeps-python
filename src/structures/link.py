from src.defs import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


def operate_links():
    for room_name in Object.keys(Game.rooms):
        room = Game.rooms[room_name]
        central_link_id = Memory.links[room_name]
        if central_link_id is undefined or get_central_link(central_link_id) is None:
            continue
        central_link = get_central_link(central_link_id)
        if central_link.energyCapacity - central_link.energy <= 0 or central_link.cooldown > 0:
            continue
        links = list(filter(lambda s: s.structureType == STRUCTURE_LINK and
                                      s.energy > 0 and
                                      s.cooldown == 0 and
                                      s.id != central_link_id,
                            room.find(FIND_MY_STRUCTURES)))
        for link in links:
            result = operate_link(link, central_link)
            if result:
                return


def get_central_link(link_id):
    return Game.getObjectById(link_id)


def operate_link(link, central_link):
    amount = min(central_link.energyCapacity - central_link.energy, link.energy)
    result = link.transferEnergy(central_link, amount)
    return True if result == OK else False
