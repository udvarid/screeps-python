from src.defs import *


def need_extra(context):
    return context.number < context.max and more_worker_would_be_useful(context)


def more_worker_would_be_useful(context):
    my_harvesters = filter(lambda c: c.memory.role == 'harvester', context.room.find(FIND_MY_CREEPS))
    sources = len(context.room.find(FIND_SOURCES))

    work_elements = 0
    for harvester in my_harvesters:
        work_elements += harvester.getActiveBodyparts(WORK)

    return work_elements // sources < 6
