from src.defs import *
from src.roles.builder import run_builder

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


def run_c_builder(creep: Creep):
    if creep.memory.role2 == 'builder':
        run_builder(creep)
        return
    if creep.memory.birth is undefined:
        creep.memory.birth = True
        __pragma__('js', '{}', 'Memory.room_conquer[creep.memory.home]["time"] = Game.time')

    if creep.memory.my_exit is undefined:
        direction = creep.room.findExitTo(creep.memory.aim)
        creep.memory.my_exit = creep.pos.findClosestByRange(direction)
        creep.memory.my_path = creep.room.findPath(creep.pos, creep.memory.my_exit)
    if creep.pos.roomName == creep.memory.aim:
        controller = creep.room.controller
        if creep.memory.cont_path is undefined or len(creep.memory.cont_path) == 0:
            creep.memory.cont_path = creep.room.findPath(creep.pos, controller.pos, {'swampCost': 1})
        if creep.pos.inRangeTo(controller, 3):
            creep.memory.role2 = 'builder'
        else:
            creep.moveByPath(creep.memory.cont_path)
    else:
        result = creep.moveByPath(creep.memory.my_path)
        if result is not OK and len(creep.memory.my_path) > 0:
            creep.memory.my_path = creep.room.findPath(creep.pos, creep.memory.my_exit)
        elif result is not OK and len(creep.memory.my_path) == 0:
            direction = creep.room.findExitTo(creep.memory.aim)
            creep.memory.my_exit = creep.pos.findClosestByRange(direction)
            creep.memory.my_path = creep.room.findPath(creep.pos, creep.memory.my_exit)


