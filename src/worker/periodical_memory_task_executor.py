from src.worker.periodical_tasks.room_safety import make_room_safety_check
from src.worker.periodical_tasks.room_snapshot import make_room_snapshot
from src.worker.periodical_tasks.memory_clean import clean_memory
from src.defs import *

__pragma__('noalias', 'undefined')


def do_periodical_tasks():
    if Memory.counters is undefined:
        Memory.counters = {}
    clean_memory()
    make_room_snapshot()
    make_room_safety_check()
