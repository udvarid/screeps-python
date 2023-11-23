from src.constant.constants import MEMORY_CLEANING
from src.defs import *


def clean_memory():
    if not Memory.clean_time or Memory.clean_time <= 0:
        console.log('memory cleaning!')
        Memory.clean_time = MEMORY_CLEANING
        for name in Object.keys(Memory.creeps):
            if not Object.keys(Game.creeps).includes(name):
                del Memory.creeps[name]
    else:
        Memory.clean_time -= 1
