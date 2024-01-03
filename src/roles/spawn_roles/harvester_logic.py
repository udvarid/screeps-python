from src.defs import *

__pragma__('noalias', 'undefined')


def need_extra(context):
    source_place = context.max
    if Memory.room_snapshot is not undefined and Memory.room_snapshot[context.room['name']] is not undefined:
        source_place = min(Memory.room_snapshot[context.room['name']]['source_place'], source_place)
    return context.number < source_place and more_worker_would_be_useful(context)


def more_worker_would_be_useful(context):
    spawns_in_room = context.room.find(FIND_MY_SPAWNS)
    for spawn_in_room in spawns_in_room:
        if spawn_in_room.spawning is not None and spawn_in_room.spawning['name'] is not undefined and \
                spawn_in_room.spawning['name'].includes("harvester"):
            return False
    my_harvesters = list(filter(lambda c: c.memory.role == 'harvester', context.room.find(FIND_MY_CREEPS)))
    sources = len(context.room.find(FIND_SOURCES))

    work_elements = 0
    for harvester in my_harvesters:
        work_elements += harvester.getActiveBodyparts(WORK)

    return work_elements // sources < 8

