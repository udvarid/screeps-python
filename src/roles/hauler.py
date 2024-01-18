from src.constant.my_constants import FILL_WITH_ENERGY, TERMINAL_MINIMUM_ENERGY, TERMINAL_MINIMUM_RESOURCE, \
    TERMINAL_MAXIMUM_ENERGY
from src.defs import *
from src.utility.helper import get_link_with_energy

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


def run_hauler(creep):
    room_name = creep.room.name
    time = Game.time
    __pragma__('js', '{}', 'Memory.room_snapshot[room_name]["hauler_time"] = time')
    if not creep.memory.working:
        if creep.ticksToLive < 50:
            creep.suicide()
        possible_target = get_target(creep)
        if check_for_real_targets(creep, possible_target):
            creep.memory.working = True
        elif check_energy_back_to_store(creep, possible_target):
            creep.memory.working = True
        elif _.sum(creep.carry) == 0:
            check_for_link_with_energy(creep)
            if creep.memory.working is False:
                check_for_resource_from_container(creep)
            if creep.memory.working is False:
                check_for_terminal_job(creep)
            if creep.memory.working is False:
                check_for_lab_job(creep)

    if creep.memory.working:
        if creep.memory.filling and _.sum(creep.carry) > 0:
            creep.memory.filling = False
        elif not creep.memory.filling and _.sum(creep.carry) <= 0:
            creep.memory.filling = True

        if creep.memory.filling:
            if creep.memory.source:

                source = Game.getObjectById(creep.memory.source)
            else:
                source = creep.room.storage
                link_with_energy = get_link_with_energy(creep.room.name)
                if link_with_energy is not None:
                    source = link_with_energy
                creep.memory.source = source.id

            if creep.pos.isNearTo(source):
                result = creep.withdraw(source, creep.memory.resource)
                if result != OK:
                    creep.memory.working = False
                else:
                    del creep.memory.source
            else:
                creep.moveTo(source, {'visualizePathStyle': {'stroke': '#ffffff'}})
        else:
            target = Game.getObjectById(creep.memory.target)
            is_close = creep.pos.isNearTo(target)
            if is_close:
                result = creep.transfer(target, creep.memory.resource)
                if result == OK or result == ERR_FULL:
                    del creep.memory.target
                    creep.memory.working = False
                else:
                    print("[{}] Unknown result from creep.transfer({}, {}): {}"
                          .format(creep.name, target, creep.memory.resource, result))
            else:
                creep.moveTo(target, {'visualizePathStyle': {'stroke': '#ffffff'}})
    else:
        spawns_in_room = creep.room.find(FIND_MY_SPAWNS)
        spawn_in_room = spawns_in_room[0]
        is_close = creep.pos.isNearTo(spawn_in_room)
        if not is_close:
            creep.moveTo(spawn_in_room, {'visualizePathStyle': {'stroke': '#ffffff'}})


def check_for_lab_job(creep):
    labs = list(filter(lambda s: s.structureType == STRUCTURE_LAB, creep.room.find(FIND_MY_STRUCTURES)))
    if len(labs) == 0:
        return
    labs_wo_energy = list(filter(lambda l: l.store.getUsedCapacity(RESOURCE_ENERGY) < 2000, labs))
    if len(labs_wo_energy) > 0:
        storage = creep.room.storage
        storage_energy = storage.store.getUsedCapacity(RESOURCE_ENERGY)
        if storage_energy > 10000:
            creep.memory.working = True
            creep.memory.filling = True
            creep.memory.resource = RESOURCE_ENERGY
            creep.memory.source = storage.id
            creep.memory.target = labs_wo_energy[0].id
    else:
        if Memory.labs is undefined or Memory.labs[creep.room.name] is undefined:
            return
        storage = creep.room.storage
        role_resource_pairs = [
            ('attack', RESOURCE_CATALYZED_UTRIUM_ACID),
            ('ranged_attack', RESOURCE_CATALYZED_KEANIUM_ALKALIDE),
            ('heal', RESOURCE_CATALYZED_LEMERGIUM_ALKALIDE),
            ('tough', RESOURCE_CATALYZED_GHODIUM_ALKALIDE)
        ]
        if any(storage.store.getUsedCapacity(rr_pair[1]) > 0 for rr_pair in role_resource_pairs):
            for rr_pair in role_resource_pairs:
                if send_resource_if_possible(rr_pair, creep, storage):
                    break


def send_resource_if_possible(rr_pair, creep, storage):
    role = rr_pair[0]
    resource = rr_pair[1]

    if storage.store.getUsedCapacity(resource) == 0:
        return False

    lab_id = Memory.labs[creep.room.name][role]
    if lab_id is undefined:
        return False
    lab = Game.getObjectById(lab_id)
    if lab is undefined:
        return False
    res_amount_in_lab = lab.store.getUsedCapacity(resource)
    if res_amount_in_lab > 1500:
        return False

    creep.memory.working = True
    creep.memory.filling = True
    creep.memory.resource = resource
    creep.memory.source = storage.id
    creep.memory.target = lab.id

    return True


def check_for_terminal_job(creep):
    terminals = list(filter(lambda s: s.structureType == STRUCTURE_TERMINAL,
                            creep.room.find(FIND_MY_STRUCTURES)))
    if len(terminals) > 0:
        terminal = terminals[0]
        storage = creep.room.storage
        terminal_energy = terminal.store.getUsedCapacity(RESOURCE_ENERGY)
        storage_energy = storage.store.getUsedCapacity(RESOURCE_ENERGY)
        resource = Memory.room_snapshot[creep.room.name]['mineral']
        terminal_resource = terminal.store.getUsedCapacity(resource)
        storage_resource = storage.store.getUsedCapacity(resource)
        if terminal_energy < TERMINAL_MINIMUM_ENERGY and storage_energy > 10000:
            creep.memory.working = True
            creep.memory.filling = True
            creep.memory.resource = RESOURCE_ENERGY
            creep.memory.source = storage.id
            creep.memory.target = terminal.id
        elif terminal_resource < TERMINAL_MINIMUM_RESOURCE and storage_resource > 0:
            creep.memory.working = True
            creep.memory.filling = True
            creep.memory.resource = resource
            creep.memory.source = storage.id
            creep.memory.target = terminal.id
        elif terminal_energy > TERMINAL_MAXIMUM_ENERGY:
            creep.memory.working = True
            creep.memory.filling = True
            creep.memory.resource = RESOURCE_ENERGY
            creep.memory.source = terminal.id
            creep.memory.target = storage.id
        elif check_for_other_mineral(creep, terminal, resource):
            creep.memory.working = True
            creep.memory.source = terminal.id
            creep.memory.target = storage.id


def check_for_other_mineral(creep, terminal, resource):
    extra_mineral = undefined
    for mineral in Object.keys(terminal.store):
        if mineral != RESOURCE_ENERGY and mineral != resource and terminal.store.getUsedCapacity(mineral) > 0:
            extra_mineral = mineral
            break
    if extra_mineral is not undefined:
        creep.memory.filling = True
        creep.memory.resource = extra_mineral
        return True
    return False


def check_for_resource_from_container(creep):
    containers = list(
        filter(lambda s: s.structureType == STRUCTURE_CONTAINER and s.store.getUsedCapacity() > 0,
               creep.room.find(FIND_STRUCTURES)))
    if len(containers) > 0:
        container_to_use = sorted(containers, key=lambda c: c.store.getFreeCapacity())[0]
        creep.memory.working = True
        creep.memory.filling = True
        creep.memory.resource = Object.keys(container_to_use.store)[0]
        creep.memory.source = container_to_use.id
        creep.memory.target = creep.room.storage.id


def check_for_link_with_energy(creep):
    link_with_energy = get_link_with_energy(creep.room.name)
    if link_with_energy is not None:
        creep.memory.working = True
        creep.memory.filling = True
        creep.memory.source = link_with_energy.id
        creep.memory.target = creep.room.storage.id
        creep.memory.resource = RESOURCE_ENERGY


def check_energy_back_to_store(creep, possible_target):
    if possible_target is None and _.sum(creep.carry) > 0:
        creep.memory.filling = False
        del creep.memory.source
        creep.memory.target = creep.room.storage.id
        creep.memory.resource = RESOURCE_ENERGY
        return True
    else:
        return False


def check_for_real_targets(creep, possible_target):
    if creep.room.storage.store[RESOURCE_ENERGY] > 0 and possible_target is not None:
        creep.memory.filling = False
        del creep.memory.source
        creep.memory.target = possible_target.id
        creep.memory.resource = RESOURCE_ENERGY
        return True
    else:
        return False


def get_target(creep):
    room = creep.room
    target = None
    if Memory.room_safety_state[room.name].enemy:
        towers = list(filter(lambda s: s.structureType == STRUCTURE_TOWER and
                                       s.energy < s.energyCapacity * 0.5, room.find(FIND_STRUCTURES)))
        target = creep.pos.findClosestByPath(towers)
    if target is None:
        structures = filter(lambda s: FILL_WITH_ENERGY.includes(s.structureType) and
                                      s.energy < s.energyCapacity * 0.75, room.find(FIND_MY_STRUCTURES))
        target = creep.pos.findClosestByPath(structures)
    return target
