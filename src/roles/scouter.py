from src.defs import *

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
        # owner
        # enemy
        # attacker
        # neighbours
        # put into memory, handling the relationships

        creep.suicide()
    creep.moveByPath(creep.memory.my_path)


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
