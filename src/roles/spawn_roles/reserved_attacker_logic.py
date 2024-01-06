from src.defs import *
from src.roles.reserved_attacker import reserved_attacker_roles

__pragma__('noalias', 'undefined')


def need_extra(context):
    room_name = context.room['name']
    if Memory.room_reserved_attack is undefined or Memory.room_reserved_attack[room_name] is undefined:
        return False
    energy_in_store = context.room.storage.store[RESOURCE_ENERGY]
    attackers = _.sum(Game.creeps,
                      lambda c: c.memory.home == room_name and reserved_attacker_roles.includes(c.memory.role))
    if attackers == 0 and energy_in_store > 25000:
        __pragma__('js', '{}', 'Memory.room_reserved_attack[room_name]["spawn_status"] = "PROGRESS"')
    if attackers == 3:
        __pragma__('js', '{}', 'Memory.room_reserved_attack[room_name]["spawn_status"] = "STOP"')
        return False
    status = Memory.room_reserved_attack[room_name]['spawn_status']
    return context.number < context.max and status == "PROGRESS"


def give_aim(room_name):
    if Memory.room_reserved_attack is not undefined and Memory.room_reserved_attack[room_name] is not undefined:
        return Memory.room_reserved_attack[room_name]['aim']
    return "NA"
