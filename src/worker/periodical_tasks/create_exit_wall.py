from src.constant.my_constants import ROOM_DEFINE_EXIT
from src.defs import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')

FIND_ME_EXITS = [FIND_EXIT_TOP, FIND_EXIT_BOTTOM, FIND_EXIT_RIGHT, FIND_EXIT_LEFT]


def create_exit_wall_plan():
    if not Memory.define_exit_time or Memory.define_exit_time <= 0:
        Memory.define_exit_time = ROOM_DEFINE_EXIT
        room_exits = Memory.room_exits
        if room_exits is undefined:
            room_exits = {}
        for room_name in Object.keys(Game.rooms):
            room = Game.rooms[room_name]
            if len(room.find(FIND_MY_SPAWNS)) > 0:
                if room_exits[room_name] is not undefined:
                    return
                exit_blocks = []
                for find_direction in FIND_ME_EXITS:
                    exits = room.find(find_direction)
                    if len(exits) > 0:
                        for exit_block in split_to_exit_blocks(exits):
                            exit_blocks.append(exit_block)

                init_walls = get_me_walls(exit_blocks, room)
                ramparts = get_rampart_from_init_walls(init_walls, room)
                final_walls = get_final_walls(init_walls, ramparts)
                exits_to_report = {
                    'exits': exit_blocks,
                    'walls': final_walls,
                    'ramparts': ramparts
                }
                __pragma__('js', '{}', 'room_exits[room_name] = exits_to_report')

        Memory.room_exits = room_exits
    else:
        Memory.define_exit_time -= 1


def split_to_exit_blocks(exits):
    result = []
    sub_list = []
    prev = undefined
    for current in map(lambda e: (e.x, e.y), exits):
        if prev == undefined:
            prev = current
            sub_list.append(current)
            continue
        if prev[0] == current[0] and abs(prev[1] - current[1]) == 1 or \
                prev[1] == current[1] and abs(prev[0] - current[0]) == 1:
            sub_list.append(current)
        else:
            result.append(sub_list[:])
            sub_list = [current]
        prev = current

    result.append(sub_list[:])
    return result


def get_me_walls(exits, room):
    result = []
    final_result = []
    for exit_block in exits:
        wall_block = []
        for exit_element in exit_block:
            if exit_element[0] == 0:
                wall_block.append((2, exit_element[1]))
            if exit_element[1] == 0:
                wall_block.append((exit_element[0], 2))
            if exit_element[0] == 49:
                wall_block.append((47, exit_element[1]))
            if exit_element[1] == 49:
                wall_block.append((exit_element[0], 47))
        first_exit = exit_block[0]
        if first_exit[0] == 0:
            wall_block.append((2, first_exit[1] - 1))
            wall_block.append((2, first_exit[1] - 2))
            wall_block.append((1, first_exit[1] - 2))
        if first_exit[1] == 0:
            wall_block.append((first_exit[0] - 1, 2))
            wall_block.append((first_exit[0] - 2, 2))
            wall_block.append((first_exit[0] - 2, 1))
        if first_exit[0] == 49:
            wall_block.append((47, first_exit[1] - 1))
            wall_block.append((47, first_exit[1] - 2))
            wall_block.append((48, first_exit[1] - 2))
        if first_exit[1] == 49:
            wall_block.append((first_exit[0] - 1, 47))
            wall_block.append((first_exit[0] - 2, 47))
            wall_block.append((first_exit[0] - 2, 48))
        last_exit = exit_block[len(exit_block) - 1]
        if last_exit[0] == 0:
            wall_block.append((2, last_exit[1] + 1))
            wall_block.append((2, last_exit[1] + 2))
            wall_block.append((1, last_exit[1] + 2))
        if last_exit[1] == 0:
            wall_block.append((last_exit[0] + 1, 2))
            wall_block.append((last_exit[0] + 2, 2))
            wall_block.append((last_exit[0] + 2, 1))
        if last_exit[0] == 49:
            wall_block.append((47, last_exit[1] + 1))
            wall_block.append((47, last_exit[1] + 2))
            wall_block.append((48, last_exit[1] + 2))
        if last_exit[1] == 49:
            wall_block.append((last_exit[0] + 1, 47))
            wall_block.append((last_exit[0] + 2, 47))
            wall_block.append((last_exit[0] + 2, 48))
        result.append(wall_block)

    for wall_block in result:
        final_block = []
        for wall in wall_block:
            terrain = room.getTerrain().get(wall[0], wall[1])
            if terrain != 1:
                final_block.append((wall[0], wall[1]))
        final_result.append(final_block)

    return final_result


def get_rampart_from_init_walls(walls, room):
    result = []
    controller = room.controller
    for wall_block in walls:
        room_positions = list(map(lambda w: __new__(RoomPosition(w[0], w[1], room.name)), wall_block))
        closest = controller.pos.findClosestByPath(room_positions)
        result.append((closest.x, closest.y))
    return result


def get_final_walls(init_walls, ramparts):
    result = []
    for i in range(len(init_walls)):
        final_wall_block = []
        rampart = ramparts[i]
        for wall in init_walls[i]:
            if not (wall[0] == rampart[0] and wall[1] == rampart[1]):
                final_wall_block.append((wall[0], wall[1]))
        result.append(final_wall_block)
    return result
