from src.roles import harvester
from src.defs import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


def operate_worker_creeps():
    for name in Object.keys(Game.creeps):
        creep = Game.creeps[name]
        # külön konstanstént egy dict-be tenni a role-okhoz tartozó fv-t, amit használni kell
        harvester.run_harvester(creep)
