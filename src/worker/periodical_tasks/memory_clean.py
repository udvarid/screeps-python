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
    if not Memory.clean_time or Memory.clean_time <= 0:
        console.log('memory cleaning!')
        Memory.clean_time = MEMORY_CLEANING
        for name in Object.keys(Memory.creeps):
            if not Object.keys(Game.creeps).includes(name):
                del Memory.creeps[name]
    else:
        Memory.clean_time -= 1
