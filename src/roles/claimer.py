from src.defs import *
from src.worker.periodical_tasks.create_construction_site import is_valid_type, is_near_to_sources, pos_in_the_frame

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


def run_claimer(creep: Creep):
    if creep.memory.birth is undefined:
        creep.memory.birth = True
        __pragma__('js', '{}', 'Memory.room_conquer[creep.memory.aim]["aim"]["time"] = Game.time')

    if creep.memory.my_exit is undefined:
        direction = creep.room.findExitTo(creep.memory.aim)
        creep.memory.my_exit = creep.pos.findClosestByRange(direction)
        creep.memory.my_path = creep.room.findPath(creep.pos, creep.memory.my_exit)
    if creep.room.name != creep.memory.home:
        controller = creep.room.controller
        if creep.memory.cont_path is undefined:
            creep.memory.cont_path = creep.room.findPath(creep.pos, controller.pos, {'swampCost': 1})

        result = creep.claimController(controller)
        if result == ERR_NOT_IN_RANGE:
            creep.moveByPath(creep.memory.cont_path)

        if controller.my:
            cont_sites = creep.room.find(FIND_CONSTRUCTION_SITES)
            spawns = creep.room.find(FIND_MY_SPAWNS)
            print("We have {} construction sites and {} spawn"
                  .format(len(cont_sites), len(spawns)))
            if len(cont_sites) == 0 and len(spawns) == 0:
                sources = creep.room.find(FIND_SOURCES)
                pos1 = (sources[0].pos.x + sources[1].pos.x) // 2
                pos2 = (sources[0].pos.y + sources[1].pos.y) // 2
                middle = (pos1, pos2)
                spawn = find_place_for_spawn(middle, creep.room)
                if spawn is not undefined:
                    print(spawn)
                    creep.room.createConstructionSite(spawn[0], spawn[1], STRUCTURE_SPAWN)
                    __pragma__('js', '{}', 'Memory.room_conquer[creep.memory.aim]["aim"]["claimed"] = True')
            if len(spawns) > 0:
                del Memory.room_conquer[creep.memory.aim]
                __pragma__('js', '{}', 'Memory.room_map[creep.room.name]["owner"] = "me"')
                creep.suicide()
                # TODO a builder legyen harvester
    else:
        result = creep.moveByPath(creep.memory.my_path)
        if result is not OK and len(creep.memory.my_path) > 0:
            creep.memory.my_path = creep.room.findPath(creep.pos, creep.memory.my_exit)
        elif result is not OK and len(creep.memory.my_path) == 0:
            direction = creep.room.findExitTo(creep.memory.aim)
            creep.memory.my_exit = creep.pos.findClosestByRange(direction)
            creep.memory.my_path = creep.room.findPath(creep.pos, creep.memory.my_exit)


def find_place_for_spawn(middle, room):
    my_queue = [middle]
    checked_elements = []
    counter = 0
    while len(my_queue) > 0 and counter < 250:
        counter += 1
        actual = my_queue.pop(0)
        checked_elements.append(actual)
        actual_is_valid_type = is_valid_type(actual, room)
        actual_is_near_to_sources = is_near_to_sources(actual, room)
        if actual_is_valid_type and not actual_is_near_to_sources:
            return actual
        neighbours = get_neighbours(actual)
        for neighbour in neighbours:
            if pos_in_the_frame(neighbour) and not any(neighbour[0] == checked_element[0] and
                                                       neighbour[1] == checked_element[1] for checked_element in
                                                       checked_elements) and \
                    not any(neighbour[0] == actual_element[0] and
                            neighbour[1] == actual_element[1] for actual_element in my_queue):
                my_queue.append(neighbour)
    return undefined


def get_neighbours(actual):
    x = actual[0]
    y = actual[1]

    n1 = (x - 1, y - 1)
    n2 = (x - 1, y)
    n3 = (x - 1, y + 1)

    n4 = (x, y - 1)
    n5 = (x, y + 1)

    n6 = (x + 1, y - 1)
    n7 = (x + 1, y)
    n8 = (x + 1, y + 1)
    return [n1, n2, n3, n4, n5, n6, n7, n8]
