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


def run_harvester(creep):
    """
    Runs a creep as a generic harvester.
    :param creep: The creep to run
    """

    # If we're full, stop filling up and remove the saved source
    if creep.memory.filling and _.sum(creep.carry) >= creep.carryCapacity:
        creep.memory.filling = False
    # If we're empty, start filling again and remove the saved target
    elif not creep.memory.filling and creep.carry.energy <= 0:
        if creep.ticksToLive < 50:
            creep.suicide()
        creep.memory.filling = True
        del creep.memory.target

    if creep.memory.filling:
        # If we have a saved source, use it
        if creep.memory.source:
            source = Game.getObjectById(creep.memory.source)
        else:
            energy_sources = creep.room.find(FIND_SOURCES)
            source_with_workers = []
            for energy_source in energy_sources:
                harvesters = list(filter(lambda c: c.memory.source == energy_source.id,
                                         creep.room.find(FIND_MY_CREEPS)))
                work_elements = 0
                for harvester in harvesters:
                    work_elements += harvester.getActiveBodyparts(WORK)
                source_with_workers.append((energy_source, work_elements))
            source = sorted(source_with_workers, key=lambda c: c[1])[0]
            creep.memory.source = source[0].id

        # If we're near the source, harvest it - otherwise, move to it.
        if creep.pos.isNearTo(source):
            creep.harvest(source)
        else:
            creep.moveTo(source, {'visualizePathStyle': {'stroke': '#ffffff'}})
    else:
        # If we have a saved target, use it
        if creep.memory.target:
            target = Game.getObjectById(creep.memory.target)
        else:
            target = get_target(creep)
            creep.memory.target = target.id

        # If we are targeting a spawn or extension, we need to be directly next to it - otherwise, we can be 3 away.
        if target.energyCapacity or target == creep.room.storage:
            is_close = creep.pos.isNearTo(target)
        else:
            is_close = creep.pos.inRangeTo(target, 3)

        if is_close:
            # If we are targeting a spawn or extension, transfer energy. Otherwise, use upgradeController on it.
            if target.energyCapacity or target == creep.room.storage:
                result = creep.transfer(target, RESOURCE_ENERGY)
                if result == OK or result == ERR_FULL:
                    del creep.memory.target
            else:
                creep.upgradeController(target)
                if not creep.pos.inRangeTo(target, 2):
                    creep.moveTo(target)
        else:
            creep.moveTo(target, {'visualizePathStyle': {'stroke': '#ffffff'}})


def get_target(creep):
    room = creep.room
    target = undefined
    hauler_time = Memory.room_snapshot[room.name]['hauler_time']
    we_have_haulers = True if hauler_time is not None and (Game.time - hauler_time) < 10 else False
    if Memory.room_safety_state[room.name] is not undefined and \
            Memory.room_safety_state[room.name].enemy and not we_have_haulers:
        target = _(room.find(FIND_STRUCTURES)) \
            .filter(lambda s: (s.structureType == STRUCTURE_TOWER and s.energy < s.energyCapacity * 0.5)).sample()
    if target is undefined and not we_have_haulers:
        target = _(room.find(FIND_STRUCTURES)) \
            .filter(lambda s: (FILL_WITH_ENERGY.includes(s.structureType) and
                               s.energy < s.energyCapacity * 0.9)).sample()
    if target is undefined:
        links = list(filter(lambda s: s.structureType == STRUCTURE_LINK and
                                      s.energyCapacity - s.energy >= creep.carry.energy,
                            creep.room.find(FIND_MY_STRUCTURES)))
        if len(links) > 0:
            target = creep.pos.findClosestByPath(links)
    if target is undefined and room.storage is not undefined:
        target = _([room.storage]).filter(lambda s: s.store[RESOURCE_ENERGY] < 200000).sample()
    if target is undefined:
        target = _(room.find(FIND_STRUCTURES)).filter(lambda s: (s.structureType == STRUCTURE_CONTROLLER)).sample()
    return target
