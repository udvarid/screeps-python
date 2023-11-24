from src.roles.harvester import run_harvester
from src.defs import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')

CREEP_TASKS = {
    'harvester': {'run_task': run_harvester}
}


def operate_worker_creeps():
    for name in Object.keys(Game.creeps):
        creep = Game.creeps[name]
        CREEP_TASKS[creep.memory.role].run_task(creep)
