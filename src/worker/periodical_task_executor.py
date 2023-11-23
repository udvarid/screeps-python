from src.worker.periodical_tasks.memory_clean import clean_memory


def do_periodical_tasks():
    clean_memory()
