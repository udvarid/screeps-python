from src.defs import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


def run_builder(creep: Creep):
    if creep.memory.building and creep.store[RESOURCE_ENERGY] == 0:
        creep.memory.building = False
    if not creep.memory.building and creep.store.getFreeCapacity() == 0:
        if creep.ticksToLive < 50:
            creep.suicide()
        creep.memory.building = True

    if creep.memory.building:
        targets = creep.room.find(FIND_CONSTRUCTION_SITES)
        if len(targets):
            if creep.build(targets[0]) == ERR_NOT_IN_RANGE:
                creep.moveTo(
                    targets[0], {'visualizePathStyle': {'stroke': '#ffffff'}})
        else:
            creep.memory.role = 'upgrader' if creep.room.storage is not undefined else 'harvester'
    else:
        storage = creep.room.storage
        if storage is not undefined and storage.store[RESOURCE_ENERGY] > 0:
            if creep.withdraw(storage, RESOURCE_ENERGY) == ERR_NOT_IN_RANGE:
                creep.moveTo(storage, {'visualizePathStyle': {'stroke': '#ffaa00'}})
        else:
            sources = list(filter(lambda s: s.energy > 0, creep.room.find(FIND_SOURCES)))
            if len(sources) > 0:
                source = creep.pos.findClosestByPath(sources)
                if creep.harvest(source) == ERR_NOT_IN_RANGE:
                    creep.moveTo(source, {'visualizePathStyle': {'stroke': '#ffaa00'}})
