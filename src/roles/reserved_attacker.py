from src.defs import *
from src.roles.builder import run_builder
from src.utility.helper import get_full_neighbours

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
        if creep.pos.roomName == creep.memory.aim:
            if creep.memory.first_time_x is undefined:
                creep.memory.first_time_x = creep.pos.x
                creep.memory.first_time_y = creep.pos.y

            if moved_from_exit(creep):
                if creep.memory.my_exit is not undefined:
                    del creep.memory.my_exit
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
                return
            else:
                if creep.pos.inRangeTo(possibly_injured, 3):
                    creep.rangedHeal(possibly_injured)
                creep.moveTo(possibly_injured.pos)
                return
        elif creep.hits < creep.hitsMax:
            creep.heal(creep)
            return
        closest_friend = creep.pos.findClosestByPath(others)
        creep.moveTo(closest_friend)
        return

    go_to_controller(creep)


def run_reserved_attacker_range(creep):
    enemies = creep.room.find(FIND_HOSTILE_CREEPS)
    attacker_enemies = list(filter(lambda c: c.getActiveBodyparts(RANGED_ATTACK) +
                                             c.getActiveBodyparts(ATTACK) > 0, enemies))
    structures = list(filter(lambda s: s.structureType != STRUCTURE_WALL and
                                       s.structureType != STRUCTURE_ROAD and
                                       s.structureType != STRUCTURE_CONTROLLER,
                             creep.room.find(FIND_STRUCTURES)))
    walls = list(filter(lambda s: s.structureType == STRUCTURE_WALL, creep.room.find(FIND_STRUCTURES)))

    close = list(filter(lambda c: c.memory.role == 'reserved_attacker_close', creep.room.find(FIND_MY_CREEPS)))
    healer = list(filter(lambda c: c.memory.role == 'reserved_attacker_heal', creep.room.find(FIND_MY_CREEPS)))

    too_far = False
    if len(close) > 0 and creep.pos.getRangeTo(close[0]) > 3:
        too_far = True

    closest_enemy = undefined
    if len(attacker_enemies) > 0:
        closest_enemy = creep.pos.findClosestByRange(attacker_enemies)
    elif len(enemies) > 0:
        closest_enemy = creep.pos.findClosestByRange(enemies)
    elif len(structures) > 0:
        closest_enemy = creep.pos.findClosestByRange(structures)
    elif len(walls) > 0:
        closest_enemy = creep.pos.findClosestByRange(walls)
    if closest_enemy is not undefined:
        if creep.pos.inRangeTo(closest_enemy, 3):
            creep.rangedAttack(closest_enemy)
            distance = creep.pos.getRangeTo(closest_enemy)
            if distance < 3:
                new_pos = get_new_pos_from_enemy(creep, closest_enemy, distance)
                if new_pos is not undefined:
                    creep.moveTo(new_pos)
                    return
            return
        elif not too_far and creep.pos.inRangeTo(closest_enemy, 6):
            creep.moveTo(closest_enemy)
            return
        if len(close) == 0 and (len(healer) == 0 or creep.hits > creep.hitsMax * 0.5):
            creep.moveTo(closest_enemy)
            return

    if len(close) > 0:
        creep.moveTo(close[0])
        return

    go_to_controller(creep)


def get_new_pos_from_enemy(creep, closest_enemy, distance):
    neighbours = get_full_neighbours((creep.pos.x, creep.pos.y))
    cleaned_neighbours = []
    for neighbour in neighbours:
        if neighbour[0] < 1 or neighbour[0] > 48 or neighbour[1] < 1 or neighbour[1] > 48:
            continue
        if creep.room.getTerrain().get(neighbour[0], neighbour[1]) != 0:
            continue
        if abs(closest_enemy.pos.x - neighbour[0]) > distance or abs(closest_enemy.pos.y - neighbour[1]) > distance:
            cleaned_neighbours.append(neighbour)
    if len(cleaned_neighbours) > 0:
        coordinate = _(cleaned_neighbours).sample()
        new_position = __new__(RoomPosition(coordinate[0], coordinate[1], creep.room.name))
        return new_position
    return undefined


def run_reserved_attacker_close(creep):
    enemies = creep.room.find(FIND_HOSTILE_CREEPS)
    attacker_enemies = list(filter(lambda c: c.getActiveBodyparts(RANGED_ATTACK) +
                                             c.getActiveBodyparts(ATTACK) > 0, enemies))
    structures = list(filter(lambda s: s.structureType != STRUCTURE_WALL and
                                       s.structureType != STRUCTURE_ROAD and
                                       s.structureType != STRUCTURE_CONTROLLER,
                             creep.room.find(FIND_STRUCTURES)))
    walls = list(filter(lambda s: s.structureType == STRUCTURE_WALL, creep.room.find(FIND_STRUCTURES)))

    healer = list(filter(lambda c: c.memory.role == 'reserved_attacker_heal', creep.room.find(FIND_MY_CREEPS)))

    closest_enemy = undefined
    if len(attacker_enemies) > 0:
        closest_enemy = creep.pos.findClosestByRange(attacker_enemies)
    elif len(enemies) > 0:
        closest_enemy = creep.pos.findClosestByRange(enemies)
    elif len(structures) > 0:
        closest_enemy = creep.pos.findClosestByRange(structures)
    elif len(walls) > 0:
        closest_enemy = creep.pos.findClosestByRange(walls)
    if closest_enemy is not undefined:
        if creep.pos.isNearTo(closest_enemy):
            creep.attack(closest_enemy)
            return
        elif len(healer) == 0 or creep.hits > creep.hitsMax * 0.5:
            creep.moveTo(closest_enemy)
            return

    const_sites = creep.room.find(FIND_CONSTRUCTION_SITES)
    if len(const_sites) > 0:
        closest_const_site = creep.pos.findClosestByPath(const_sites)
        creep.moveTo(closest_const_site)
        return

    go_to_controller(creep)


def go_to_controller(creep):
    if creep.hits <= creep.hitsMax * 0.5:
        return
    controller = creep.room.controller
    close_to_controller = creep.pos.inRangeTo(controller, 3)
    if not close_to_controller:
        if creep.memory.cont_path is undefined or len(creep.memory.cont_path) == 0:
            creep.memory.cont_path = creep.room.findPath(creep.pos, controller.pos, {'swampCost': 1})
        result = creep.moveByPath(creep.memory.cont_path)
        if result is not OK:
            del creep.memory.cont_path
