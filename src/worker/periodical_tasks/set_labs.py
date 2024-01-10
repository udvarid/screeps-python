from src.constant.my_constants import ROOM_SET_LABS
from src.defs import *
from src.utility.helper import get_active_rooms

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


def set_labs():
    if not Memory.counters["room_set_labs_time"] or Memory.counters["room_set_labs_time"] <= 0:
        time_limit = ROOM_SET_LABS
        __pragma__('js', '{}', 'Memory.counters["room_set_labs_time"] = time_limit')
        for room_name in get_active_rooms():
            room = Game.rooms[room_name]
            labs = list(filter(lambda s: s.structureType == STRUCTURE_LAB, room.find(FIND_MY_STRUCTURES)))
            if len(labs) < 4:
                continue
            if Memory.labs is undefined or Memory.labs[room_name] is undefined:
                print('No lab memory, new is setting')
                fill_up_memory(labs, room_name)
            else:
                print('Labs are in memory, checking them')
                checked_and_good = True
                lab_ids = list(map(lambda l: l.id, labs))
                lab_memory_ids = []
                for memory_lab in Object.keys(Memory.labs[room_name]):
                    lab_memory_ids.append(Memory.labs[room_name][memory_lab])
                for lab_id in lab_ids:
                    if not lab_memory_ids.includes(lab_id):
                        del Memory.labs[room_name]
                        checked_and_good = False
                        fill_up_memory(labs, room_name)
                        break
                if checked_and_good:
                    print('Labs are ok, no change is necessary')
                else:
                    print('Labs are not ok, rewrote memory')
    else:
        actual = Memory.counters["room_set_labs_time"]
        __pragma__('js', '{}', 'Memory.counters["room_set_labs_time"] = actual - 1')


def fill_up_memory(labs, room_name):
    if Memory.labs is undefined:
        Memory.labs = {}
    roles = [ATTACK, RANGED_ATTACK, HEAL, TOUGH]
    lab_ids = list(map(lambda l: l.id, labs))

    roles_with_ids = []

    possible_attacker = list(filter(lambda l: l.store.getUsedCapacity(RESOURCE_CATALYZED_UTRIUM_ACID) > 0, labs))
    possible_r_attacker = list(filter(lambda l: l.store.getUsedCapacity(RESOURCE_CATALYZED_KEANIUM_ALKALIDE) > 0, labs))
    possible_healer = list(filter(lambda l: l.store.getUsedCapacity(RESOURCE_CATALYZED_LEMERGIUM_ALKALIDE) > 0, labs))
    possible_tougher = list(filter(lambda l: l.store.getUsedCapacity(RESOURCE_CATALYZED_GHODIUM_ALKALIDE) > 0, labs))

    if len(possible_attacker) > 0:
        lab_id = possible_attacker[0].id
        roles.remove(ATTACK)
        lab_ids.remove(lab_id)
        roles_with_ids.append((ATTACK, lab_id))

    if len(possible_r_attacker) > 0:
        lab_id = possible_r_attacker[0].id
        roles.remove(RANGED_ATTACK)
        lab_ids.remove(lab_id)
        roles_with_ids.append((RANGED_ATTACK, lab_id))

    if len(possible_healer) > 0:
        lab_id = possible_healer[0].id
        roles.remove(HEAL)
        lab_ids.remove(lab_id)
        roles_with_ids.append((HEAL, lab_id))

    if len(possible_tougher) > 0:
        lab_id = possible_tougher[0].id
        roles.remove(TOUGH)
        lab_ids.remove(lab_id)
        roles_with_ids.append((TOUGH, lab_id))

    for i in range(len(roles)):
        roles_with_ids.append((roles[i], lab_ids[i]))

    snapshot = {
        'attack': list(filter(lambda r: r[0] == ATTACK, roles_with_ids))[0][1],
        'ranged_attack ': list(filter(lambda r: r[0] == RANGED_ATTACK, roles_with_ids))[0][1],
        'heal': list(filter(lambda r: r[0] == HEAL, roles_with_ids))[0][1],
        'tough': list(filter(lambda r: r[0] == TOUGH, roles_with_ids))[0][1]
    }

    __pragma__('js', '{}', 'Memory.labs[room_name] = snapshot')


