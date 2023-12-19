from src.defs import *
from src.worker.periodical_tasks.check_for_new_rooms import get_neighbours

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


def run_scouter(creep: Creep):
    if creep.memory.my_exit is undefined:
        creep.memory.my_exit = get_exit(creep)
        creep.memory.my_path = creep.room.findPath(creep.pos, creep.memory.my_exit)
    if creep.room.name != creep.memory.home:
        energy = len(creep.room.find(FIND_SOURCES))
        owner = get_owner(creep.room)
        previous_state = Memory.room_map[creep.room.name]
        if previous_state is undefined or previous_state['neighbours'] is undefined:
            neighbours = get_neighbours(creep.room)
        else:
            neighbours = previous_state['neighbours']
        direction = reverse_direction(creep.memory.aim)
        my_home = creep.memory.home
        __pragma__('js', '{}', 'neighbours[direction] = my_home')

        enemies = creep.room.find(FIND_HOSTILE_CREEPS)
        attacker_enemies = list(filter(lambda c: c.getActiveBodyparts(RANGED_ATTACK) +
                                                 c.getActiveBodyparts(ATTACK) > 0, enemies))
        room_state = {
            'energy': energy,
            'owner': owner,
            'enemy': len(enemies) > 0,
            'attacker': len(attacker_enemies) > 0,
            'neighbours': neighbours,
            'time': Game.time
        }
        __pragma__('js', '{}', 'Memory.room_map[creep.room.name] = room_state')
        __pragma__('js', '{}', 'Memory.room_map[my_home]["neighbours"][creep.memory.aim] = creep.room.name')
        creep.suicide()
    result = creep.moveByPath(creep.memory.my_path)
    if result is not OK and len(creep.memory.my_path) > 0:
        creep.memory.my_path = creep.room.findPath(creep.pos, creep.memory.my_exit)
    elif result is not OK and len(creep.memory.my_path) == 0:
        creep.memory.my_exit = get_exit(creep)
        creep.memory.my_path = creep.room.findPath(creep.pos, creep.memory.my_exit)


def get_exit(creep):
    direction = creep.memory.aim
    if direction == "up":
        return _(creep.room.find(FIND_EXIT_TOP)).sample()
    if direction == "bottom":
        return _(creep.room.find(FIND_EXIT_BOTTOM)).sample()
    if direction == "right":
        return _(creep.room.find(FIND_EXIT_RIGHT)).sample()
    if direction == "left":
        return _(creep.room.find(FIND_EXIT_LEFT)).sample()


def get_owner(room):
    owner = 'free'
    controller = room.controller
    if controller.my:
        owner = "me"
    elif controller.owner is not undefined:
        owner = "occupied"
    elif controller.reservation is not undefined:
        owner = "reserved"
    return owner


def reverse_direction(direction):
    if direction == "up":
        return "bottom"
    if direction == "bottom":
        return "up"
    if direction == "right":
        return "left"
    if direction == "left":
        return "right"
