from src.defs import *

__pragma__('noalias', 'undefined')


def need_extra(context):
    mine_place = context.max
    if Memory.room_snapshot is not undefined and Memory.room_snapshot[context.room['name']] is not undefined:
        mine_place = min(Memory.room_snapshot[context.room['name']]['mine_place'], mine_place)
    return context.number < mine_place and more_miner_is_needed(context)


def more_miner_is_needed(context):
    extractors = list(filter(lambda s: s.structureType == STRUCTURE_EXTRACTOR, context.room.find(FIND_MY_STRUCTURES)))
    mine = context.room.find(FIND_MINERALS)[0]
    storage = context.room.storage
    return len(extractors) > 0 and mine.mineralAmount > 0 and storage is not undefined
