from src.defs import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


def run_safe_mode_claimer(creep):
    if creep.memory.filled is undefined:
        creep.memory.filled = False

    if not creep.memory.filled:
        source = creep.room.storage
        if creep.pos.isNearTo(source):
            result = creep.withdraw(source, RESOURCE_GHODIUM, 1000)
            if result == OK:
                creep.memory.filled = True
        else:
            creep.moveTo(source, {'reusePath': 15, 'visualizePathStyle': {'stroke': '#ffffff'}})
    else:
        target = creep.room.controller
        if creep.pos.isNearTo(target):
            result = creep.generateSafeMode(target)
            if result == OK:
                creep.memory.role = 'hauler'
        else:
            creep.moveTo(target, {'reusePath': 15, 'visualizePathStyle': {'stroke': '#ffffff'}})
