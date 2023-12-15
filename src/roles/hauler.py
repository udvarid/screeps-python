from src.constant.my_constants import FILL_WITH_ENERGY, TERMINAL_MINIMUM_ENERGY, TERMINAL_MINIMUM_RESOURCE
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
        if creep.ticksToLive < 20:
            creep.suicide()
        energy_in_store = creep.room.storage.store[RESOURCE_ENERGY]
        possible_target = get_target(creep)
        if energy_in_store > 10000 and possible_target is not None:
            creep.memory.working = True
            creep.memory.filling = False
            creep.memory.target = possible_target.id
            creep.memory.resource = RESOURCE_ENERGY
        if possible_target is None and _.sum(creep.carry) > 0:
            creep.memory.working = True
            creep.memory.filling = False
            creep.memory.target = creep.room.storage.id
            creep.memory.resource = RESOURCE_ENERGY
        if possible_target is None and _.sum(creep.carry) == 0:
            central_link_id = Memory.links[creep.room.name]
            if central_link_id is not undefined:
                link = Game.getObjectById(central_link_id)
                if link is not None and link.energy > 0:
                    creep.memory.working = True
                    creep.memory.filling = True
                    creep.memory.source = link.id
                    creep.memory.target = creep.room.storage.id
                    creep.memory.resource = RESOURCE_ENERGY
        if possible_target is None and _.sum(creep.carry) == 0 and creep.memory.working is False:
            containers = list(filter(lambda s: s.structureType == STRUCTURE_CONTAINER and s.store.getUsedCapacity() > 0,
                                     creep.room.find(FIND_STRUCTURES)))
            if len(containers) > 0:
                container_to_use = sorted(containers, key=lambda c: c.store.getFreeCapacity())[0]
                creep.memory.working = True
                creep.memory.filling = True
                creep.memory.resource = Memory.room_snapshot[creep.room.name]['mineral']
                creep.memory.source = container_to_use.id
                creep.memory.target = creep.room.storage.id
        if possible_target is None and _.sum(creep.carry) == 0 and creep.memory.working is False:
            terminals = list(filter(lambda s: s.structureType == STRUCTURE_TERMINAL,
                                    creep.room.find(FIND_MY_STRUCTURES)))
            if len(terminals) > 0:
                terminal = terminals[0]
                storage = creep.room.storage
                terminal_energy = terminal.store.getUsedCapacity(RESOURCE_ENERGY)
                storage_energy = storage.store.getUsedCapacity(RESOURCE_ENERGY)
                resource = Memory.room_snapshot[creep.room.name]['mineral']
                terminal_resource = terminal.store.getUsedCapacity(resource)
                storage_resource = storage.store.getUsedCapacity(resource)
                if terminal_energy < TERMINAL_MINIMUM_ENERGY and storage_energy > 10000:
                    creep.memory.working = True
                    creep.memory.filling = True
                    creep.memory.resource = RESOURCE_ENERGY
                    creep.memory.source = storage.id
                    creep.memory.target = terminal.id
                elif terminal_resource < TERMINAL_MINIMUM_RESOURCE and storage_resource > 0:
                    creep.memory.working = True
                    creep.memory.filling = True
                    creep.memory.resource = resource
                    creep.memory.source = storage.id
                    creep.memory.target = terminal.id

    if creep.memory.working:
        if creep.memory.filling and _.sum(creep.carry) > 0:
            creep.memory.filling = False
        elif not creep.memory.filling and _.sum(creep.carry) <= 0:
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
                result = creep.withdraw(source, creep.memory.resource)
                if result != OK:
                    creep.memory.working = False
                else:
                    del creep.memory.source
            else:
                creep.moveTo(source, {'visualizePathStyle': {'stroke': '#ffffff'}})
        else:
            target = Game.getObjectById(creep.memory.target)
            is_close = creep.pos.isNearTo(target)
            if is_close:
                result = creep.transfer(target, creep.memory.resource)
                if result == OK or result == ERR_FULL:
                    del creep.memory.target
                    creep.memory.working = False
                else:
                    print("[{}] Unknown result from creep.transfer({}, {}): {}"
                          .format(creep.name, target, creep.memory.resource, result))
            else:
                creep.moveTo(target, {'visualizePathStyle': {'stroke': '#ffffff'}})


def get_target(creep):
    room = creep.room
    target = None
    if Memory.room_safety_state[room.name].enemy:
        towers = list(filter(lambda s: s.structureType == STRUCTURE_TOWER and
                                       s.energy < s.energyCapacity * 0.5, room.find(FIND_STRUCTURES)))
        target = creep.pos.findClosestByPath(towers)
    if target is None:
        structures = filter(lambda s: FILL_WITH_ENERGY.includes(s.structureType) and
                                      s.energy < s.energyCapacity * 0.9, room.find(FIND_MY_STRUCTURES))
        target = creep.pos.findClosestByPath(structures)
    return target
