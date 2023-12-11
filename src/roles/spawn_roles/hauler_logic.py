from src.constant.my_constants import FILL_WITH_ENERGY
from src.defs import *


def need_extra(context):
    return context.number < context.max and more_hauler_is_needed(context)


def more_hauler_is_needed(context):
    energy_in_store = context.room.storage.store[RESOURCE_ENERGY]
    structures_need_energy = filter(lambda s: FILL_WITH_ENERGY.includes(s.structureType),
                                    context.room.find(FIND_MY_CONSTRUCTION_SITES))
    return energy_in_store > 10000 and (context.number == 0 or len(structures_need_energy) > 45)
