from src.defs import *


def need_extra(context):
    return context.number < context.max and more_upgrader_is_needed(context)


def more_upgrader_is_needed(context):
    energy_in_store = context.room.storage.store[RESOURCE_ENERGY]
    return context.number == 0 and energy_in_store > 10000 or context.number > 0 and energy_in_store > 200000
