from src.constant.my_constants import MEMORY_CLEANING
from src.defs import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


def clean_memory():
    if not Memory.counters["clean_time"] or Memory.counters["clean_time"] <= 0:
        console.log('memory cleaning!')
        time_limit = MEMORY_CLEANING
        __pragma__('js', '{}', 'Memory.counters["clean_time"] = time_limit')
        for name in Object.keys(Memory.creeps):
            if not Object.keys(Game.creeps).includes(name):
                del Memory.creeps[name]
    else:
        actual = Memory.counters["clean_time"]
        __pragma__('js', '{}', 'Memory.counters["clean_time"] = actual - 1')
