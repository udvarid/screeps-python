from src.defs import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


def need_extra(context):
    return context.number < context.max and more_claimer_is_needed(context)


def more_claimer_is_needed(context):
    return Memory.room_conquer is not undefined and Memory.room_conquer[context.room['name']] is not undefined


def give_aim(room_name):
    if Memory.room_conquer is not undefined and Memory.room_conquer[room_name] is not undefined:
        return Memory.room_conquer[room_name]['aim']
    return "NA"
