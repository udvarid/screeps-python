from src.constant.my_constants import FILL_WITH_ENERGY
from src.defs import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


def run_hauler(creep):
    room_name = creep.room.name
    time = Game.time
    __pragma__('js', '{}', 'Memory.room_snapshot[room_name]["hauler_time"] = time')
    if not creep.memory.working:
        energy_in_store = creep.room.storage.store[RESOURCE_ENERGY]
        possible_target = get_target(creep)
        if energy_in_store > 10000 and possible_target is not None:
            creep.memory.working = True
            creep.memory.filling = False
            creep.memory.target = possible_target.id
        if possible_target is None and _.sum(creep.carry) > 0:
            creep.memory.working = True
            creep.memory.filling = False
            creep.memory.target = creep.room.storage.id
        if possible_target is None and _.sum(creep.carry) == 0:
            central_link_id = Memory.links[creep.room.name]
            if central_link_id is not undefined:
                link = Game.getObjectById(central_link_id)
                if link is not None and link.energy > 0:
                    creep.memory.working = True
                    creep.memory.filling = True
                    creep.memory.source = link.id
                    creep.memory.target = creep.room.storage.id

    if creep.memory.working:
        if creep.memory.filling and _.sum(creep.carry) > 0:
            creep.memory.filling = False
        elif not creep.memory.filling and creep.carry.energy <= 0:
            creep.memory.filling = True

        if creep.memory.filling:
            if creep.memory.source:
                source = Game.getObjectById(creep.memory.source)
            else:
                source = creep.room.storage
                central_link_id = Memory.links[creep.room.name]
                if central_link_id is not undefined:
                    link = Game.getObjectById(central_link_id)
                    if link is not None and link.energy > 0:
                        source = link
                creep.memory.source = source.id

            if creep.pos.isNearTo(source):
                result = creep.withdraw(source, RESOURCE_ENERGY)
                if result != OK:
                    print("[{}] Unknown result from creep.withdraw from storage ({}): {}".format(creep.name, source,
                                                                                                 result))
                else:
                    del creep.memory.source
            else:
                creep.moveTo(source, {'visualizePathStyle': {'stroke': '#ffffff'}})
        else:
            target = Game.getObjectById(creep.memory.target)
            is_close = creep.pos.isNearTo(target)
            if is_close:
                result = creep.transfer(target, RESOURCE_ENERGY)
                if result == OK or result == ERR_FULL:
                    del creep.memory.target
                    creep.memory.working = False
                else:
                    print("[{}] Unknown result from creep.transfer({}, {}): {}"
                          .format(creep.name, target, RESOURCE_ENERGY, result))
            else:
                creep.moveTo(target, {'visualizePathStyle': {'stroke': '#ffffff'}})


def get_target(creep):
    room = creep.room
    target = None
    if Memory.room_safety_state[room.name].enemy:
        towers = filter(lambda s: s.structureType == STRUCTURE_TOWER and s.energy < s.energyCapacity * 0.5, room.find(FIND_STRUCTURES))
        target = creep.pos.findClosestByPath(towers)
    if target is None:
        structures = filter(lambda s: FILL_WITH_ENERGY.includes(s.structureType) and
                                         s.energy < s.energyCapacity * 0.9, room.find(FIND_MY_STRUCTURES))
        target = creep.pos.findClosestByPath(structures)
    return target
