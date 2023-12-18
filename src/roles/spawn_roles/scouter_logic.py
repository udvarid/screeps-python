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
    return context.number < context.max and more_scouter_is_needed(context)


def more_scouter_is_needed(context):
    if Memory.room_map is undefined or Memory.room_map[context.room.name] is undefined:
        return False
    room_state = Memory.room_map[context.room.name]
    is_uncharted = room_state['neighbours']['up'] == "?" or \
                   room_state['neighbours']['bottom'] == "?" or \
                   room_state['neighbours']['right'] == "?" or \
                   room_state['neighbours']['left'] == "?"
    # TODO később itt lehet olyan, hogy kikeressük azon szobákat, melyeket nem mi birtoklunk és régen térképeztük fel
    return is_uncharted


def give_aim(room_name):
    room_state = Memory.room_map[room_name]
    up = room_state['neighbours']['up']
    bottom = room_state['neighbours']['bottom']
    right = room_state['neighbours']['right']
    left = room_state['neighbours']['left']
    if up == "?":
        return "up"
    elif bottom == "?":
        return "bottom"
    elif right == "?":
        return "right"
    elif left == "?":
        return "left"
    # TODO később itt lehet olyan, hogy kikeressük azon szobákat, melyeket nem mi birtoklunk és régen térképeztük fel
    return "NA"
