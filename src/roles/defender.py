from src.defs import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


def run_defender(creep: Creep):
    if creep.memory.birth is undefined:
        creep.memory.birth = True
        __pragma__('js', '{}', 'Memory.room_conquer[creep.memory.home]["time"] = Game.time')

    if creep.pos.roomName == creep.memory.aim:
        if creep.memory.first_time_x is undefined:
            creep.memory.first_time_x = creep.pos.x
            creep.memory.first_time_y = creep.pos.y

        if moved_from_exit(creep):
            defend_room(creep)
        else:
            controller = creep.room.controller
            if creep.memory.cont_path is undefined or len(creep.memory.cont_path) == 0:
                creep.memory.cont_path = creep.room.findPath(creep.pos, controller.pos, {'swampCost': 1})
            result = creep.moveByPath(creep.memory.cont_path)
            if result is not OK:
                del creep.memory.cont_path

    else:
        if creep.memory.my_exit is undefined:
            direction = creep.room.findExitTo(creep.memory.aim)
            creep.memory.my_exit = creep.pos.findClosestByRange(direction)
            creep.memory.my_path = creep.room.findPath(creep.pos, creep.memory.my_exit)
        if creep.memory.first_time_x is not undefined:
            del creep.memory.first_time_x
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


def defend_room(creep):
    if Memory.room_conquer[creep.memory.home] is not undefined:
        towers = list(filter(lambda s: s.structureType == STRUCTURE_TOWER, creep.room.find(FIND_MY_STRUCTURES)))
        if len(towers) > 0:
            del Memory.room_conquer[creep.memory.home]

    if creep.hits < creep.hitsMax * 0.5:
        creep.heal(creep)
        return

    closest_enemy = get_closest_enemy(creep)

    if closest_enemy is not undefined:
        if not creep.pos.isNearTo(closest_enemy) and creep.pos.inRangeTo(closest_enemy, 3):
            creep.rangedAttack(closest_enemy)
            creep.moveTo(closest_enemy)
            return
        elif creep.pos.isNearTo(closest_enemy):
            creep.attack(closest_enemy)
            return
        elif not creep.pos.inRangeTo(closest_enemy, 3):
            creep.moveTo(closest_enemy)
    else:
        enemy_structures = list(filter(lambda s: s.structureType != STRUCTURE_WALL and not s.my,
                                       creep.room.find(FIND_STRUCTURES)))
        if len(enemy_structures) > 0:
            closest_structure = creep.pos.findClosestByPath(enemy_structures)
            if creep.pos.isNearTo(closest_structure):
                creep.attack(closest_structure)
            else:
                creep.moveTo(closest_structure)
            return

    go_to_controller(creep)


def get_closest_enemy(creep):
    enemies = creep.room.find(FIND_HOSTILE_CREEPS)
    attacker_enemies = list(filter(lambda c: c.getActiveBodyparts(RANGED_ATTACK) +
                                             c.getActiveBodyparts(ATTACK) > 0, enemies))

    closest_enemy = undefined
    if len(attacker_enemies) > 0:
        closest_enemy = creep.pos.findClosestByRange(attacker_enemies)
    elif len(enemies) > 0:
        closest_enemy = creep.pos.findClosestByRange(enemies)

    return closest_enemy


def go_to_controller(creep):
    controller = creep.room.controller
    close_to_controller = creep.pos.inRangeTo(controller, 3)
    if not close_to_controller:
        if creep.memory.cont_path is undefined or len(creep.memory.cont_path) == 0:
            creep.memory.cont_path = creep.room.findPath(creep.pos, controller.pos, {'swampCost': 1})
        result = creep.moveByPath(creep.memory.cont_path)
        if result is not OK:
            del creep.memory.cont_path
