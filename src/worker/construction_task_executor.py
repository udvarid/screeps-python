from src.worker.periodical_tasks.build_containers import construct_containers
from src.worker.periodical_tasks.build_exit_wall import build_exit_wall
from src.worker.periodical_tasks.build_links import construct_links
from src.worker.periodical_tasks.build_mine import construct_mine
from src.worker.periodical_tasks.clear_unknown_walls import clear_walls
from src.worker.periodical_tasks.create_construction_site import create_construction_site
from src.worker.periodical_tasks.create_exit_wall import create_exit_wall_plan
from src.worker.periodical_tasks.create_rampart import create_rampart
from src.worker.periodical_tasks.set_labs import set_labs


def check_for_new_rampart():
    create_rampart()


def check_for_new_construction_site():
    create_construction_site()


def exit_wall_plan_creator():
    create_exit_wall_plan()


def exit_wall_builder():
    build_exit_wall()


def clear_unknown_walls():
    clear_walls()


def build_links():
    construct_links()


def build_mine():
    construct_mine()


def build_containers():
    construct_containers()


def set_labs_to_memory():
    set_labs()
