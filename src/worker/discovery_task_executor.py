from src.worker.periodical_tasks.check_for_new_conquers import check_for_new_conquers
from src.worker.periodical_tasks.check_for_new_reserved_attack import check_for_new_reserved_attack
from src.worker.periodical_tasks.check_for_new_scouts import check_for_new_scouts


def check_rooms_for_scout():
    check_for_new_scouts()


def check_rooms_for_conquer():
    check_for_new_conquers()


def check_rooms_for_reserved_attack():
    check_for_new_reserved_attack()
