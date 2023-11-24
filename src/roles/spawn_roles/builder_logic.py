from src.defs import *


def need_extra(context):
    construction_sites = context.room.find(FIND_MY_CONSTRUCTION_SITES)
    return len(construction_sites) > 0
