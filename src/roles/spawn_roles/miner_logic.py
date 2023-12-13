from src.defs import *

__pragma__('noalias', 'undefined')


def need_extra(context):
    return context.number < context.max and more_miner_is_needed(context)


def more_miner_is_needed(context):
    extractors = list(filter(lambda s: s.structureType == STRUCTURE_EXTRACTOR, context.room.find(FIND_MY_STRUCTURES)))
    mine = context.room.find(FIND_MINERALS)[0]
    storage = context.room.storage
    return len(extractors) > 0 and mine.mineralAmount > 0 and storage is not undefined
