from src.worker.periodical_tasks.room_snapshot import make_room_snapshot
from src.worker.periodical_tasks.memory_clean import clean_memory


def do_periodical_tasks():
    clean_memory()
    make_room_snapshot()
