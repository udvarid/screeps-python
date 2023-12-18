from src.defs import *


def need_extra(context):
    return context.number < context.max and more_builder_is_needed(context)


def more_builder_is_needed(context):
    construction_sites = context.room.find(FIND_MY_CONSTRUCTION_SITES)
    return context.number == 0 and len(construction_sites) > 0
