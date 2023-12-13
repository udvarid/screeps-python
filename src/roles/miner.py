from src.defs import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


def run_miner(creep):
    if not creep.memory.source:
        creep.memory.source = creep.room.find(FIND_MINERALS)[0].id
        creep.memory.mineral = Memory.room_snapshot[creep.room.name]['mineral']

    if creep.memory.filling and _.sum(creep.carry) >= creep.carryCapacity:
        creep.memory.filling = False
    elif not creep.memory.filling and _.sum(creep.carry) <= 0:
        if creep.ticksToLive < 300 or creep.room.find(FIND_MINERALS)[0].mineralAmount == 0:
            creep.memory.role = 'harvester'
            return
        creep.memory.filling = True
        del creep.memory.target

    if creep.memory.filling:
        source = Game.getObjectById(creep.memory.source)
        if creep.pos.isNearTo(source):
            result = creep.harvest(source)
            if result == ERR_NOT_ENOUGH_RESOURCES:
                creep.memory.filling = False
        else:
            creep.moveTo(source, {'visualizePathStyle': {'stroke': '#ffffff'}})
    else:
        if creep.memory.target:
            target = Game.getObjectById(creep.memory.target)
        else:
            target = get_target(creep)
            creep.memory.target = target.id

        if creep.pos.isNearTo(target):
            result = creep.transfer(target, creep.memory.mineral)
            if result == OK or result == ERR_FULL:
                del creep.memory.target
        else:
            creep.moveTo(target, {'visualizePathStyle': {'stroke': '#ffffff'}})


def get_target(creep):
    target = creep.room.storage
    return target
