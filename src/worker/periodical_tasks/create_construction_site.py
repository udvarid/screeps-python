from src.constant.my_constants import ROOM_CONSTRUCTION, STRUCTURES_NEED_CONSTRUCT
from src.defs import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


def create_construction_site():
    if not Memory.counters["construction_time"] or Memory.counters["construction_time"] <= 0:
        time_limit = ROOM_CONSTRUCTION
        __pragma__('js', '{}', 'Memory.counters["construction_time"] = time_limit')
        for room_name in Object.keys(Game.rooms):
            room = Game.rooms[room_name]
            spawns = room.find(FIND_MY_SPAWNS)
            if len(spawns) > 0 and room.controller.my and \
                    not Memory.room_safety_state[room_name].enemy and \
                    len(room.find(FIND_MY_CONSTRUCTION_SITES)) == 0:
                for structure in STRUCTURES_NEED_CONSTRUCT:
                    structures = list(filter(lambda s: s.structureType == structure, room.find(FIND_MY_STRUCTURES)))
                    max_number = CONTROLLER_STRUCTURES[structure][room.controller.level]
                    if max_number > len(structures):
                        print("{} room tries to structure {}".format(room_name, structure))
                        find_and_create_construction_site(spawns[0], structure)
                        return
    else:
        actual = Memory.counters["construction_time"]
        __pragma__('js', '{}', 'Memory.counters["construction_time"] = actual - 1')


def find_and_create_construction_site(spawn, structure):
    all_structures = spawn.room.find(FIND_STRUCTURES)
    my_queue = [(spawn.pos.x, spawn.pos.y)]
    checked_elements = []
    found_construction_site = False
    while len(my_queue) > 0 and not found_construction_site:
        actual = my_queue.pop(0)
        checked_elements.append(actual)
        actual_is_valid_type = is_valid_type(actual, spawn.room)
        actual_is_occupied = any(actual[0] == struct.pos.x and actual[1] == struct.pos.y for struct in all_structures)
        actual_is_near_to_sources = is_near_to_sources(actual, spawn.room)
        if not actual_is_occupied and actual_is_valid_type and not actual_is_near_to_sources:
            spawn.room.createConstructionSite(actual[0], actual[1], structure)
            found_construction_site = True
            continue
        if actual_is_valid_type:
            neighbours = get_neighbours(actual)
            for neighbour in neighbours:
                if pos_in_the_frame(neighbour) and not any(neighbour[0] == checked_element[0] and
                                                           neighbour[1] == checked_element[1] for checked_element in
                                                           checked_elements) and \
                        not any(neighbour[0] == actual_element[0] and
                                neighbour[1] == actual_element[1] for actual_element in my_queue):
                    my_queue.append(neighbour)


def pos_in_the_frame(position):
    return not (position[0] <= 2 or position[0] >= 47 or position[1] <= 2 or position[1] >= 47)


def is_near_to_sources(actual, room):
    act_pos = __new__(RoomPosition(actual[0], actual[1], room.name))
    mineral = room.find(FIND_MINERALS)[0]
    if act_pos.isNearTo(mineral):
        return True
    for source in room.find(FIND_SOURCES):
        if act_pos.isNearTo(source):
            return True
    return False


def get_neighbours(actual):
    x = actual[0]
    y = actual[1]
    n1 = (x - 1, y - 1)
    n2 = (x - 1, y + 1)
    n3 = (x + 1, y - 1)
    n4 = (x + 1, y + 1)
    return [n1, n2, n3, n4]


def is_valid_type(actual, room):
    terrain_type = room.getTerrain().get(actual[0], actual[1])
    if terrain_type == 0 or terrain_type == 2:
        return True
    return False
