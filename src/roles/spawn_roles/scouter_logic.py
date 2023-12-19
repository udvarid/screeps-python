from src.defs import *
from src.utility.helper import get_active_rooms

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
    has_uncharted_neighbour = room_state['neighbours']['up'] == "?" or \
                              room_state['neighbours']['bottom'] == "?" or \
                              room_state['neighbours']['right'] == "?" or \
                              room_state['neighbours']['left'] == "?"
    neighbour_scouted_long_ago = get_neighbour_scouted_long_ago(context.room.name)
    return has_uncharted_neighbour or neighbour_scouted_long_ago is not undefined


def get_neighbour_scouted_long_ago(room_name):
    room_state = Memory.room_map[room_name]
    not_room = ["?", "NO"]
    neighbours = []
    if not not_room.includes(room_state['neighbours']['up']):
        neighbours.append(('up', room_state['neighbours']['up']))
    if not not_room.includes(room_state['neighbours']['bottom']):
        neighbours.append(('bottom', room_state['neighbours']['bottom']))
    if not not_room.includes(room_state['neighbours']['right']):
        neighbours.append(('right', room_state['neighbours']['right']))
    if not not_room.includes(room_state['neighbours']['left']):
        neighbours.append(('left', room_state['neighbours']['left']))

    if len(neighbours) > 0:
        my_rooms = get_active_rooms()

        for neigh in neighbours:
            if any(neigh[1] == room for room in my_rooms):
                continue
            scout_time = Memory.room_map[neigh[1]]['time']
            if Game.time - scout_time > 15000:
                return neigh[0]

    return undefined


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
    neighbour_scouted_long_ago = get_neighbour_scouted_long_ago(room_name)
    if neighbour_scouted_long_ago is not undefined:
        return neighbour_scouted_long_ago
    return "NA"
