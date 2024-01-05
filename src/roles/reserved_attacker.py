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
        if creep.pos.roomName == creep.memory.aim:
            if creep.memory.first_time_x is undefined:
                creep.memory.first_time_x = creep.pos.x
                creep.memory.first_time_y = creep.pos.y

            if moved_from_exit(creep):
                del creep.memory.first_time_x
                if creep.memory.role == "reserved_attacker_close":
                    run_reserved_attacker_close(creep)
                elif creep.memory.role == "reserved_attacker_range":
                    run_reserved_attacker_range(creep)
                elif creep.memory.role == "reserved_attacker_heal":
                    run_reserved_attacker_heal(creep)
            else:
                controller = creep.room.controller
                if creep.memory.cont_path is undefined or len(creep.memory.cont_path) == 0:
                    creep.memory.cont_path = creep.room.findPath(creep.pos, controller.pos, {'swampCost': 1})
                result = creep.moveByPath(creep.memory.cont_path)
                if result is not OK:
                    del creep.memory.cont_path
        else:
            result = creep.moveByPath(creep.memory.my_path)
            if result is not OK and len(creep.memory.my_path) > 0:
                creep.memory.my_path = creep.room.findPath(creep.pos, creep.memory.my_exit)
            elif result is not OK and len(creep.memory.my_path) == 0:
                direction = creep.room.findExitTo(creep.memory.aim)
                creep.memory.my_exit = creep.pos.findClosestByPath(direction)
                creep.memory.my_path = creep.room.findPath(creep.pos, creep.memory.my_exit)


def moved_from_exit(creep):
    return abs(creep.memory.first_time_x - creep.pos.x) >= 2 or \
        abs(creep.memory.first_time_y - creep.pos.y) >= 2


def run_reserved_attacker_heal(creep):
    if creep.hits < creep.hitsMax * 0.75:
        creep.heal(creep)
        return
    others = list(filter(lambda c: c.memory.role == 'reserved_attacker_close' or
                                   c.memory.role == 'reserved_attacker_range', creep.room.find(FIND_MY_CREEPS)))
    if len(others) > 0:
        possibly_injured = sorted(others, key=lambda c: c.hits / c.hits.hitsMax)[0]
        if possibly_injured.hits < possibly_injured.hitsMax:
            if creep.pos.isNearTo(possibly_injured.pos):
                creep.heal(possibly_injured)
            else:
                if creep.pos.inRangeTo(possibly_injured, 3):
                    creep.rangedHeal(possibly_injured)
                creep.moveTo(possibly_injured.pos)
        elif creep.hits < creep.hitsMax:
            creep.heal(creep)
            return
        closest_friend = creep.pos.findClosestByPath(others)
        creep.moveTo(closest_friend.pos)
        return



    go_to_controller(creep)


def run_reserved_attacker_range(creep):
    enemies = creep.room.find(FIND_HOSTILE_CREEPS)
    attacker_enemies = list(filter(lambda c: c.getActiveBodyparts(RANGED_ATTACK) +
                                             c.getActiveBodyparts(ATTACK) > 0, enemies))
    structures = list(filter(lambda s: s.structureType != STRUCTURE_WALL, creep.room.find(FIND_STRUCTURES)))

    others = list(filter(lambda c: c.memory.role == 'reserved_attacker_close', creep.room.find(FIND_MY_CREEPS)))
    too_far = False
    if len(others) > 0 and creep.pos.getRangeTo(others[0]) > 3:
        too_far = True

    closest_enemy = undefined
    if len(attacker_enemies) > 0:
        closest_enemy = creep.pos.findClosestByRange(attacker_enemies)
    elif len(enemies) > 0:
        closest_enemy = creep.pos.findClosestByRange(enemies)
    elif len(structures) > 0:
        closest_enemy = creep.pos.findClosestByRange(structures)
    if closest_enemy is not undefined:
        if creep.pos.inRangeTo(closest_enemy, 3):
            creep.rangedAttack(closest_enemy)
            return
        elif not too_far and creep.pos.inRangeTo(closest_enemy, 6):
            creep.moveTo(closest_enemy)
            return
        if len(others) == 0:
            creep.moveTo(closest_enemy)
            return

    if len(others) > 0:
        creep.moveTo(others[0])
        return

    go_to_controller(creep)


def run_reserved_attacker_close(creep):
    enemies = creep.room.find(FIND_HOSTILE_CREEPS)
    attacker_enemies = list(filter(lambda c: c.getActiveBodyparts(RANGED_ATTACK) +
                                             c.getActiveBodyparts(ATTACK) > 0, enemies))
    structures = list(filter(lambda s: s.structureType != STRUCTURE_WALL, creep.room.find(FIND_STRUCTURES)))

    closest_enemy = undefined
    if len(attacker_enemies) > 0:
        closest_enemy = creep.pos.findClosestByRange(attacker_enemies)
    elif len(enemies) > 0:
        closest_enemy = creep.pos.findClosestByRange(enemies)
    elif len(structures) > 0:
        closest_enemy = creep.pos.findClosestByRange(structures)
    if closest_enemy is not undefined:
        if creep.pos.isNearTo(closest_enemy):
            creep.attack(closest_enemy)
            return
        else:
            creep.moveTo(closest_enemy)
            return

    go_to_controller(creep)


def go_to_controller(creep):
    controller = creep.room.controller
    close_to_controller = creep.pos.inRangeTo(controller, 3)
    if not close_to_controller:
        if creep.memory.cont_path is undefined or len(creep.memory.cont_path) == 0:
            creep.memory.cont_path = creep.room.findPath(creep.pos, controller.pos, {'swampCost': 1})
        result = creep.moveByPath(creep.memory.cont_path)
        if result is not OK:
            del creep.memory.cont_path
