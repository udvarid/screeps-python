from src.defs import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


def run_c_builder(creep: Creep):
    if creep.memory.birth is undefined:
        creep.memory.birth = True
        __pragma__('js', '{}', 'Memory.room_conquer[creep.memory.aim]["aim"]["time"] = Game.time')

    if creep.memory.my_exit is undefined:
        direction = creep.room.findExitTo(creep.memory.aim)
        creep.memory.my_exit = creep.pos.findClosestByRange(direction)
        creep.memory.my_path = creep.room.findPath(creep.pos, creep.memory.my_exit)
    if creep.room.name != creep.memory.home:
        # TODO energiát gyűjteni, construction-t felépíteni
        # TODO ha kész, beállni harvesternek ide
        pass
    else:
        result = creep.moveByPath(creep.memory.my_path)
        if result is not OK and len(creep.memory.my_path) > 0:
            creep.memory.my_path = creep.room.findPath(creep.pos, creep.memory.my_exit)
        elif result is not OK and len(creep.memory.my_path) == 0:
            direction = creep.room.findExitTo(creep.memory.aim)
            creep.memory.my_exit = creep.pos.findClosestByRange(direction)
            creep.memory.my_path = creep.room.findPath(creep.pos, creep.memory.my_exit)


