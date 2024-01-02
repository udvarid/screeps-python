from src.constant.my_constants import MINIMUM_SAFE_MODE_NUMBER
from src.defs import *

__pragma__('noalias', 'undefined')


def need_extra(context):
    return context.number < context.max and more_safe_mode_claimer_is_needed(context)


def more_safe_mode_claimer_is_needed(context):
    if context.room.controller.safeModeAvailable >= MINIMUM_SAFE_MODE_NUMBER:
        return False
    if context.room.storage is undefined:
        return False
    ghodium_in_store = context.room.storage.store[RESOURCE_GHODIUM]
    return ghodium_in_store >= 1000
