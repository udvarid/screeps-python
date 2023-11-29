from src.worker.periodical_tasks.create_construction_site import create_construction_site
from src.worker.periodical_tasks.create_rampart import create_rampart


def check_for_new_rampart():
    create_rampart()


def check_for_new_construction_site():
    create_construction_site()
