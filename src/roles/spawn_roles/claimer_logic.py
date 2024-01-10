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
    room_name = context.room['name']
    if Memory.room_conquer is undefined or Memory.room_conquer[room_name] is undefined:
        return False
    aim_room = Memory.room_conquer[room_name]['aim']
    aim_status = Memory.room_map[aim_room]['owner']
    return aim_status != "me"


def give_aim(room_name):
    if Memory.room_conquer is not undefined and Memory.room_conquer[room_name] is not undefined:
        return Memory.room_conquer[room_name]['aim']
    return "NA"
