from src.structures.tower import operate_towers
from src.worker import periodical_memory_task_executor
from src.worker import construction_task_executor
from src.worker import spawn_executor
from src.worker import worker_creep_job_assign_executor


def do_periodical_tasks():
    periodical_memory_task_executor.do_periodical_tasks()
    construction_task_executor.check_for_new_rampart()


def do_strategic_tasks():
    operate_towers()


def do_spawning():
    spawn_executor.do_spawn()


def do_creep_related_tasks():
    worker_creep_job_assign_executor.operate_worker_creeps()
