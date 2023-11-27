from src.constant.my_constants import STRUCTURE_WALL_OR_RAMPART_OR_ROAD, STRUCTURE_WALL_OR_RAMPART, \
    RAMPART_AND_WALL_SIZE
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
    if Memory.room_safety_state[tower.room.name].enemy and attack_enemy(tower):
        return
    # TODO csak akkor csinálja ezeket, ha legalább 25%ig van az energia, többit védelemre
    if Memory.room_safety_state[tower.room.name].wounded_creeps and heal_friend(tower):
        return
    if Memory.room_safety_state[tower.room.name].wounded_struc and repair_structure(tower):
        return
    build_rampart_and_wall(tower)


def attack_enemy(tower):
    closest_enemy = tower.pos.findClosestByRange(FIND_HOSTILE_CREEPS)
    if closest_enemy is not None:
        tower.attack(closest_enemy)
        return True
    return False


def heal_friend(tower):
    damaged_creep = _(tower.room.find(FIND_MY_CREEPS)) \
        .filter(lambda c: c.hits < c.hitsMax) \
        .sample()
    if damaged_creep is not undefined:
        tower.heal(damaged_creep)
        return True
    return False


def repair_structure(tower):
    damaged_structure = _(tower.room.find(FIND_MY_STRUCTURES)) \
        .filter(lambda s: s.hits < s.hitsMax and not STRUCTURE_WALL_OR_RAMPART_OR_ROAD.includes(s.structureType)) \
        .sample()
    if damaged_structure is not undefined:
        tower.repair(damaged_structure)
        return True
    return False


def build_rampart_and_wall(tower):
    hit_level = RAMPART_AND_WALL_SIZE[tower.room.controller.level - 1]
    wall_or_rampart = filter(lambda s: STRUCTURE_WALL_OR_RAMPART.includes(s.structureType) and s.hits < hit_level,
                             tower.room.find(FIND_MY_STRUCTURES))
    if len(wall_or_rampart) > 0:
        structure_to_repair = sorted(wall_or_rampart, key=lambda c: c.hits)[0]
        tower.repair(structure_to_repair)


