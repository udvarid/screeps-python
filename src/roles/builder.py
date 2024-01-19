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
        if creep.memory.target:
            target = Game.getObjectById(creep.memory.target)
        else:
            possible_targets = creep.room.find(FIND_CONSTRUCTION_SITES)
            if len(possible_targets) > 0:
                target = possible_targets[0]
                creep.memory.target = target.id
            else:
                target = None

        if target is not None:
            if creep.build(target) == ERR_NOT_IN_RANGE:
                creep.moveTo(
                    target, {'visualizePathStyle': {'stroke': '#ffffff'}})
        else:
            del creep.memory.target
            del creep.memory.source
            creep.memory.role = 'upgrader' if creep.room.storage is not undefined else 'harvester'
    else:
        if creep.memory.source:
            source = Game.getObjectById(creep.memory.source)
        else:
            storage = creep.room.storage
            if storage is not undefined and storage.store.getUsedCapacity(RESOURCE_ENERGY) > 0:
                source = storage
                creep.memory.source_type = 'storage'
            else:
                sources = creep.room.find(FIND_SOURCES)
                source = creep.pos.findClosestByPath(sources)
                creep.memory.source_type = 'source'

            creep.memory.source = source.id

        if creep.memory.source_type == 'storage':
            if source.store.getUsedCapacity(RESOURCE_ENERGY) == 0:
                del creep.memory.source
            if creep.withdraw(source, RESOURCE_ENERGY) == ERR_NOT_IN_RANGE:
                creep.moveTo(source, {'visualizePathStyle': {'stroke': '#ffaa00'}})
        else:
            if creep.harvest(source) == ERR_NOT_IN_RANGE:
                creep.moveTo(source, {'visualizePathStyle': {'stroke': '#ffaa00'}})
