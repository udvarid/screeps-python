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

reserved_attacker_roles = [
    "reserved_attacker_close",
    "reserved_attacker_range",
    "reserved_attacker_heal"
]


def run_reserved_attacker(creep: Creep):
    if creep.memory.group_formed is undefined:
        creep.memory.group_formed = False

    if creep.memory.ready_to_attack is undefined:
        creep.memory.ready_to_attack = False

    if not creep.memory.ready_to_attack:
        target = creep.room.controller
        is_close = creep.pos.inRangeTo(target, 2)

        if is_close:
            attackers = list(filter(lambda c: reserved_attacker_roles.includes(c.memory.role),
                                    creep.pos.findInRange(FIND_MY_CREEPS, 5)))
            if not creep.memory.group_formed and len(attackers) == 3:
                creep.memory.group_formed = True
            attackers_formed = list(filter(lambda c: reserved_attacker_roles.includes(c.memory.role) and
                                           c.memory.group_formed is True,
                                    creep.pos.findInRange(FIND_MY_CREEPS, 5)))
            if len(attackers_formed) == 3:
                creep.memory.ready_to_attack = True
        else:
            creep.moveTo(target, {'reusePath': 3})
    else:
        if creep.memory.my_exit is undefined:
            direction = creep.room.findExitTo(creep.memory.aim)
            creep.memory.my_exit = creep.pos.findClosestByRange(direction)
            creep.memory.my_path = creep.room.findPath(creep.pos, creep.memory.my_exit)
        if creep.pos.roomName != creep.memory.home:
            # ha először léptem be, eltávolodni innét, majd utána a roletól függő szerepeket játszani
            controller = creep.room.controller
            if creep.memory.cont_path is undefined or len(creep.memory.cont_path) == 0:
                creep.memory.cont_path = creep.room.findPath(creep.pos, controller.pos, {'swampCost': 1})
            if creep.pos.inRangeTo(controller, 3):
                creep.say("!")
            else:
                creep.moveByPath(creep.memory.cont_path)
        else:
            result = creep.moveByPath(creep.memory.my_path)
            if result is not OK and len(creep.memory.my_path) > 0:
                creep.memory.my_path = creep.room.findPath(creep.pos, creep.memory.my_exit)
            elif result is not OK and len(creep.memory.my_path) == 0:
                creep.memory.error_move = creep.memory.error_move + 1
                direction = creep.room.findExitTo(creep.memory.aim)
                creep.memory.my_exit = creep.pos.findClosestByPath(direction)
                creep.memory.my_path = creep.room.findPath(creep.pos, creep.memory.my_exit)
