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
    """
    Runs a creep as a generic harvester.
    :param creep: The creep to run
    """

    # If we're full, stop filling up and remove the saved source
    if creep.memory.filling and _.sum(creep.carry) >= creep.carryCapacity:
        creep.memory.filling = False
        del creep.memory.source
    # If we're empty, start filling again and remove the saved target
    elif not creep.memory.filling and creep.carry.energy <= 0:
        creep.memory.filling = True
        del creep.memory.target

    if creep.memory.filling:
        if creep.memory.source:
            source = Game.getObjectById(creep.memory.source)
        else:
            source = creep.room.storage
            creep.memory.source = source.id

        if creep.pos.isNearTo(source):
            result = creep.withdraw(source, RESOURCE_ENERGY)
            if result != OK:
                print("[{}] Unknown result from creep.withdraw from storage ({}): {}".format(creep.name, source, result))
        else:
            creep.moveTo(source, {'visualizePathStyle': {'stroke': '#ffffff'}})
    else:
        # If we have a saved target, use it
        if creep.memory.target:
            target = Game.getObjectById(creep.memory.target)
        else:
            target = creep.room.controller
            creep.memory.target = target.id

        is_close = creep.pos.inRangeTo(target, 3)

        if is_close:
            result = creep.upgradeController(target)
            if result != OK:
                print("[{}] Unknown result from creep.upgradeController({}): {}".format(
                    creep.name, target, result))
            # Let the creeps get a little bit closer than required to the controller, to make room for other creeps.
            if not creep.pos.inRangeTo(target, 2):
                creep.moveTo(target)
        else:
            creep.moveTo(target, {'visualizePathStyle': {'stroke': '#ffffff'}})
