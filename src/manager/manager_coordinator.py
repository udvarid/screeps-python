from src.worker import periodical_task_executor
from src.worker import spawn_executor
from src.worker import worker_creep_job_assign_executor


def do_periodical_tasks():
    periodical_task_executor.do_periodical_tasks()


def do_strategic_tasks():
    pass


def do_spawning():
    spawn_executor.do_spawn()


def do_creep_related_tasks():
    worker_creep_job_assign_executor.operate_worker_creeps()
