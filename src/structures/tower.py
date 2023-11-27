from src.constant.my_constants import STRUCTURE_NOT_TO_HEAL
from src.defs import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


def operate_towers():
    for room_name in Object.keys(Game.rooms):
        room = Game.rooms[room_name]
        towers = filter(lambda s: s.structureType == STRUCTURE_TOWER and s.energyCapacity > 0,
                        room.find(FIND_MY_STRUCTURES))
        for tower in towers:
            operate_tower(tower)


def operate_tower(tower):
    if attack_enemy(tower):
        return
    if heal_friend(tower):
        return
    if repair_structure(tower):
        return

    # TODO build rampart and walls


def attack_enemy(tower):
    if Memory.room_safety_state[tower.room.name].enemy:
        closest_enemy = tower.pos.findClosestByRange(FIND_HOSTILE_CREEPS)
        if closest_enemy is not None:
            tower.attack(closest_enemy)
            return True
    return False


def heal_friend(tower):
    # TODO csekkolni memória alapján, hogy van e sérült creep
    damaged_creep = _(tower.room.find(FIND_MY_CREEPS)) \
        .filter(lambda c: c.hits < c.hitsMax) \
        .sample()
    if damaged_creep is not undefined:
        tower.heal(damaged_creep)
        return True
    return False


def repair_structure(tower):
    # TODO csekkolni memória alapján, hogy van e sérült structure
    damaged_structure = _(tower.room.find(FIND_MY_STRUCTURES)) \
        .filter(lambda s: s.hits < s.hitsMax and not STRUCTURE_NOT_TO_HEAL.includes(s.structureType)) \
        .sample()
    if damaged_structure is not undefined:
        tower.repair(damaged_structure)
        return True
    return False
