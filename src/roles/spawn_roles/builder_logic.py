from src.defs import *


def need_extra(context):
    construction_sites = context.room.find(FIND_MY_CONSTRUCTION_SITES)
    # TODO itt azért megnézni, hogy van e már más builder, vagy akár a normál mapbe beletenni egy max változót
    return len(construction_sites) > 0
