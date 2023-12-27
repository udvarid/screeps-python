from src.constant.my_constants import ROOM_CREATE_EXIT, RAMPART_AND_WALL_SIZE, STRUCTURE_WALL_OR_RAMPART
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


def build_exit_wall():
    if not Memory.counters["create_exit_time"] or Memory.counters["create_exit_time"] <= 0:
        time_limit = ROOM_CREATE_EXIT
        __pragma__('js', '{}', 'Memory.counters["create_exit_time"] = time_limit')
        for room_name in Object.keys(Game.rooms):
            room = Game.rooms[room_name]
            if room.controller.level < 7:
                continue
            room_exits = Memory.room_exits[room_name]
            if len(room.find(FIND_MY_SPAWNS)) == 0 or room_exits is undefined:
                continue
            if Memory.room_safety_state[room_name].enemy:
                continue
            if len(room.find(FIND_MY_CONSTRUCTION_SITES)) > 0:
                continue
            if room.storage is undefined or room.storage.store.getUsedCapacity(RESOURCE_ENERGY) < 200000:
                continue
            if not Memory.room_clear[room_name]:
                continue
            hit_level = RAMPART_AND_WALL_SIZE[room.controller.level - 1] * 0.9
            wall_or_rampart = list(
                filter(lambda s: STRUCTURE_WALL_OR_RAMPART.includes(s.structureType) and s.hits < hit_level,
                       room.find(FIND_STRUCTURES)))
            if len(wall_or_rampart) > 0:
                continue

            number_to_build = 5
            wall_blocks = room_exits['walls']
            walls_in_room = list(filter(lambda s: s.structureType == STRUCTURE_WALL, room.find(FIND_STRUCTURES)))
            for wall_block in wall_blocks:
                for wall in wall_block:
                    if any(wall[0] == wall_in_room.pos.x and wall[1] == wall_in_room.pos.y
                           for wall_in_room in walls_in_room):
                        continue
                    print("Creating wall at {} in room {}".format(wall, room_name))
                    room.createConstructionSite(wall[0], wall[1], STRUCTURE_WALL)
                    number_to_build -= 1
                    if number_to_build == 0:
                        break
                if number_to_build == 0:
                    break
            if number_to_build == 0:
                continue

            ramparts_blocks = room_exits['ramparts']
            ramparts_in_room = list(
                filter(lambda s: s.structureType == STRUCTURE_RAMPART, room.find(FIND_MY_STRUCTURES)))
            for rampart in ramparts_blocks:
                if any(rampart[0] == rampart_in_room.pos.x and rampart[1] == rampart_in_room.pos.y
                       for rampart_in_room in ramparts_in_room):
                    continue
                print("Creating rampart at {} in room {}".format(rampart, room_name))
                room.createConstructionSite(rampart[0], rampart[1], STRUCTURE_RAMPART)
                number_to_build -= 1
                if number_to_build == 0:
                    break

    else:
        actual = Memory.counters["create_exit_time"]
        __pragma__('js', '{}', 'Memory.counters["create_exit_time"] = actual - 1')
