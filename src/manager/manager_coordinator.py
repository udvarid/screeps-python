from src.structures.link import operate_links
from src.structures.terminal import operate_terminals
from src.structures.tower import operate_towers
from src.worker import periodical_memory_task_executor, discovery_task_executor
from src.worker import construction_task_executor
from src.worker import spawn_executor
from src.worker import worker_creep_job_assign_executor


def do_periodical_tasks():
    periodical_memory_task_executor.do_periodical_tasks()
    construction_task_executor.check_for_new_rampart()
    construction_task_executor.check_for_new_construction_site()
    construction_task_executor.clear_unknown_walls()
    construction_task_executor.build_links()
    construction_task_executor.build_mine()
    construction_task_executor.build_containers()
    construction_task_executor.exit_wall_plan_creator()
    construction_task_executor.exit_wall_builder()


def do_strategic_tasks():
    discovery_task_executor.check_rooms_for_scout()
    discovery_task_executor.check_rooms_for_conquer()
    discovery_task_executor.check_rooms_for_reserved_attack()


def do_structure_related_tasks():
    operate_towers()
    operate_links()
    operate_terminals()


def do_spawning():
    spawn_executor.do_spawn()


def do_creep_related_tasks():
    worker_creep_job_assign_executor.operate_worker_creeps()
