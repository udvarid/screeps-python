from src.defs import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


def run_upgrader(creep):
    if creep.memory.filling and _.sum(creep.carry) >= creep.carryCapacity:
        creep.memory.filling = False
        del creep.memory.source
    elif not creep.memory.filling and creep.carry.energy <= 0:
        if creep.ticksToLive < 50:
            creep.suicide()
        creep.memory.filling = True
        del creep.memory.target

    if creep.memory.filling:
        if creep.memory.source:
            source = Game.getObjectById(creep.memory.source)
        else:
            source = creep.room.storage
            creep.memory.source = source.id

        if source.store.getUsedCapacity(RESOURCE_ENERGY) > 0:
            if creep.pos.isNearTo(source):
                creep.withdraw(source, RESOURCE_ENERGY)
            else:
                creep.moveTo(source, {'reusePath': 15, 'visualizePathStyle': {'stroke': '#ffffff'}})
        else:
            creep.moveTo(creep.room.controller)
    else:
        # If we have a saved target, use it
        if creep.memory.target:
            target = Game.getObjectById(creep.memory.target)
        else:
            target = creep.room.controller
            creep.memory.target = target.id

        # route_maintaining(creep)

        is_close = creep.pos.inRangeTo(target, 3)

        if is_close:
            creep.upgradeController(target)
            if not creep.pos.inRangeTo(target, 2):
                creep.moveTo(target, {'reusePath': 15, 'visualizePathStyle': {'stroke': '#ffffff'}})
        else:
            creep.moveTo(target, {'reusePath': 15, 'visualizePathStyle': {'stroke': '#ffffff'}})
