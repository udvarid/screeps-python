from src.defs import *

__pragma__('noalias', 'undefined')


def need_extra(context):
    return context.number < context.max and more_upgrader_is_needed(context)


def more_upgrader_is_needed(context):
    if context.room.storage is undefined:
        return False
    energy_in_store = context.room.storage.store[RESOURCE_ENERGY]
    return context.number == 0 and energy_in_store > 10000 or \
        context.number <= 1 and energy_in_store > 250000 or \
        context.number <= 2 and energy_in_store > 500000
